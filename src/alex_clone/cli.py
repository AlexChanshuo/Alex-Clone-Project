"""Command line interface for Alex Clone V1."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

from .config import GroupConfig, load_config
from .io import read_events_jsonl
from .line_personal import PersonalLineSendPlan
from .models import SendAudit
from .policy import build_reply_draft
from .report import generate_daily_report
from .vault import VaultWriter, utcish_now


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = load_config(Path(args.repo_root).resolve() if args.repo_root else Path.cwd())
    return args.func(args, config)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alex-clone")
    parser.add_argument("--repo-root", help="Repo root. Defaults to current directory.")
    subparsers = parser.add_subparsers(required=True)

    status = subparsers.add_parser("status", help="Show loaded config and vault status.")
    status.set_defaults(func=cmd_status)

    groups = subparsers.add_parser("groups", help="List approved/follow-up LINE groups.")
    groups.add_argument("--tag", help="Filter by tag, e.g. BNI, AI, family, Friends.")
    groups.set_defaults(func=cmd_groups)

    ingest = subparsers.add_parser("ingest-manual", help="Append JSONL LINE events to alex-mind raw inbox.")
    ingest.add_argument("events_jsonl", type=Path)
    ingest.set_defaults(func=cmd_ingest_manual)

    report = subparsers.add_parser("daily-report", help="Generate and optionally save daily report.")
    report.add_argument("events_jsonl", type=Path)
    report.add_argument("--date", default=date.today().isoformat())
    report.add_argument("--save", action="store_true", help="Write report into alex-mind.")
    report.set_defaults(func=cmd_daily_report)

    draft = subparsers.add_parser("draft-reply", help="Create a policy-gated reply draft.")
    draft.add_argument("--group", required=True)
    draft.add_argument("--message", required=True)
    draft.add_argument("--person")
    draft.add_argument("--intent", default="reply")
    draft.add_argument("--calendar-checked", action="store_true")
    draft.set_defaults(func=cmd_draft_reply)

    send_plan = subparsers.add_parser("personal-line-send-plan", help="Create personal LINE UI steps.")
    send_plan.add_argument("--group", required=True)
    send_plan.add_argument("--message", required=True)
    send_plan.add_argument("--confirmed", action="store_true")
    send_plan.add_argument("--audit", action="store_true", help="Write a send audit record.")
    send_plan.set_defaults(func=cmd_personal_line_send_plan)

    return parser


def cmd_status(args: argparse.Namespace, config) -> int:
    payload = {
        "repo_root": str(config.repo_root),
        "vault_dir": str(config.vault_dir),
        "vault_exists": config.vault_dir.exists(),
        "groups": [group.__dict__ for group in config.groups],
        "policy": {
            "require_confirmation_for": sorted(config.policy.require_confirmation_for),
            "allow_auto_send_for": sorted(config.policy.allow_auto_send_for),
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_groups(args: argparse.Namespace, config) -> int:
    groups = config.groups
    if args.tag:
        wanted = args.tag.casefold()
        groups = [group for group in groups if any(tag.casefold() == wanted for tag in group.tags)]
    payload = [
        {
            "display_name": group.display_name,
            "slug": group.slug,
            "tags": group.tags,
            "aliases": group.aliases,
            "status": group.status,
            "mode": group.mode,
            "daily_report": group.daily_report,
            "ingestion_adapter": group.ingestion_adapter,
        }
        for group in groups
    ]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_ingest_manual(args: argparse.Namespace, config) -> int:
    events = read_events_jsonl(args.events_jsonl)
    writer = VaultWriter(config.vault_dir)
    writer.ensure_ready()
    paths = [writer.append_raw_line_event(event) for event in events]
    unique_paths = sorted({str(path) for path in paths})
    print(json.dumps({"events_ingested": len(events), "paths": unique_paths}, ensure_ascii=False, indent=2))
    return 0


def cmd_daily_report(args: argparse.Namespace, config) -> int:
    events = read_events_jsonl(args.events_jsonl)
    report_date = date.fromisoformat(args.date)
    markdown = generate_daily_report(events, report_date=report_date)
    if args.save:
        writer = VaultWriter(config.vault_dir)
        writer.ensure_ready()
        report_path = writer.write_daily_report(report_date, markdown)
        digest_path = writer.append_interaction_digest(report_date, markdown)
        print(
            json.dumps(
                {"report_path": str(report_path), "digest_path": str(digest_path)},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(markdown)
    return 0


def cmd_draft_reply(args: argparse.Namespace, config) -> int:
    group = find_group(args.group, config.groups)
    draft = build_reply_draft(
        target_group=args.group,
        text=args.message,
        group=group,
        policy=config.policy,
        target_person=args.person,
        intent=args.intent,
        calendar_checked=args.calendar_checked,
    )
    print(json.dumps(draft.__dict__, ensure_ascii=False, indent=2))
    return 0


def cmd_personal_line_send_plan(args: argparse.Namespace, config) -> int:
    group = find_group(args.group, config.groups)
    draft = build_reply_draft(
        target_group=args.group,
        text=args.message,
        group=group,
        policy=config.policy,
        intent="reply",
    )
    if draft.policy_decision not in {"auto_send_allowed", "ask_confirm"}:
        print(json.dumps({"blocked": True, "draft": draft.__dict__}, ensure_ascii=False, indent=2))
        return 2
    if draft.policy_decision == "ask_confirm" and not args.confirmed:
        print(
            json.dumps(
                {
                    "needs_confirmation": True,
                    "draft": draft.__dict__,
                    "next_step": "Re-run with --confirmed after Alex approves.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    plan = PersonalLineSendPlan(target_group=args.group, message=args.message)
    payload = {"send_plan": plan.as_steps(), "draft": draft.__dict__}
    if args.audit:
        audit = SendAudit(
            timestamp=utcish_now(),
            target_group=args.group,
            command="personal-line-send-plan",
            message_hash=hashlib.sha256(args.message.encode("utf-8")).hexdigest(),
            policy_decision=draft.policy_decision,
            confirmation_required=draft.policy_decision == "ask_confirm",
        )
        path = VaultWriter(config.vault_dir).append_send_audit(audit)
        payload["audit_path"] = str(path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def find_group(name: str, groups: list[GroupConfig]) -> GroupConfig | None:
    normalized = name.casefold()
    for group in groups:
        candidates = {group.display_name.casefold(), group.slug.casefold()}
        candidates.update(alias.casefold() for alias in group.aliases)
        if normalized in candidates:
            return group
    return None


if __name__ == "__main__":
    raise SystemExit(main())
