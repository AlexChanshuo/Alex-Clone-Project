"""Command line interface for Alex Clone V1."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

from .checkpoint import CheckpointStore, checkpoint_summary, filter_new_events
from .config import GroupConfig, load_config
from .commands import command_guidance, parse_command
from .io import read_events_jsonl
from .line_personal import PersonalLineFetchPlan, PersonalLineSendPlan
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

    interpret = subparsers.add_parser("interpret-command", help="Parse Telegram-style natural language.")
    interpret.add_argument("text")
    interpret.set_defaults(func=cmd_interpret_command)

    guide = subparsers.add_parser("guide", help="Show natural-language command examples.")
    guide.set_defaults(func=cmd_guide)

    fetch_plan = subparsers.add_parser("fetch-plan", help="Create personal LINE fetch plans.")
    fetch_target = fetch_plan.add_mutually_exclusive_group(required=True)
    fetch_target.add_argument("--group", help="Group display name, slug, or alias.")
    fetch_target.add_argument("--tag", help="Tag to fetch, e.g. BNI, AI, family, Friends.")
    fetch_plan.add_argument("--max-scrolls", type=int, default=6)
    fetch_plan.add_argument("--capture-limit", type=int, default=80)
    fetch_plan.set_defaults(func=cmd_fetch_plan)

    checkpoints = subparsers.add_parser("checkpoints", help="Show LINE fetch checkpoints.")
    checkpoints.set_defaults(func=cmd_checkpoints)

    ingest = subparsers.add_parser("ingest-manual", help="Append JSONL LINE events to alex-mind raw inbox.")
    ingest.add_argument("events_jsonl", type=Path)
    ingest.add_argument("--new-only", action="store_true", help="Skip events older than checkpoints.")
    ingest.add_argument("--update-checkpoint", action="store_true", help="Update group checkpoints after ingest.")
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
        "state_dir": str(config.state_dir),
        "vault_exists": config.vault_dir.exists(),
        "telegram_bot_username": config.telegram_bot_username,
        "telegram_bot_configured": config.telegram_bot_configured,
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


def cmd_interpret_command(args: argparse.Namespace, config) -> int:
    parsed = parse_command(args.text, config.groups)
    print(json.dumps(parsed.__dict__, ensure_ascii=False, indent=2))
    return 0


def cmd_guide(args: argparse.Namespace, config) -> int:
    print(command_guidance())
    return 0


def cmd_fetch_plan(args: argparse.Namespace, config) -> int:
    groups = resolve_target_groups(args.group, args.tag, config.groups)
    if not groups:
        print(json.dumps({"error": "No approved group matched target."}, ensure_ascii=False, indent=2))
        return 2

    checkpoint_store = CheckpointStore(config.state_dir)
    plans = []
    for group in groups:
        checkpoint = checkpoint_store.get(group.slug)
        plan = PersonalLineFetchPlan.from_group(
            group,
            checkpoint=checkpoint,
            max_scrolls=args.max_scrolls,
            capture_limit=args.capture_limit,
        )
        plans.append(
            {
                "group": group.display_name,
                "slug": group.slug,
                "tags": group.tags,
                "checkpoint": checkpoint_summary(checkpoint),
                "steps": plan.as_steps(),
            }
        )
    print(json.dumps({"fetch_plans": plans}, ensure_ascii=False, indent=2))
    return 0


def cmd_checkpoints(args: argparse.Namespace, config) -> int:
    checkpoint_store = CheckpointStore(config.state_dir)
    checkpoints = checkpoint_store.load_all()
    payload = {
        group.slug: {
            "group": group.display_name,
            "tags": group.tags,
            **checkpoint_summary(checkpoints.get(group.slug)),
        }
        for group in config.groups
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_ingest_manual(args: argparse.Namespace, config) -> int:
    events = read_events_jsonl(args.events_jsonl)
    checkpoint_store = CheckpointStore(config.state_dir)
    if args.new_only:
        events = filter_events_by_config_checkpoints(events, config.groups, checkpoint_store)
    writer = VaultWriter(config.vault_dir)
    writer.ensure_ready()
    paths = [writer.append_raw_line_event(event) for event in events]
    unique_paths = sorted({str(path) for path in paths})
    updated_checkpoints = []
    if args.update_checkpoint:
        for group in config.groups:
            checkpoint = checkpoint_store.update_from_events(group, events)
            updated_checkpoints.append({group.slug: checkpoint_summary(checkpoint)})
    print(
        json.dumps(
            {
                "events_ingested": len(events),
                "paths": unique_paths,
                "updated_checkpoints": updated_checkpoints,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
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


def resolve_target_groups(group_name: str | None, tag: str | None, groups: list[GroupConfig]) -> list[GroupConfig]:
    if group_name:
        group = find_group(group_name, groups)
        return [group] if group and group.status == "approved" else []
    if tag:
        wanted = tag.casefold()
        return [
            group
            for group in groups
            if group.status == "approved" and any(item.casefold() == wanted for item in group.tags)
        ]
    return []


def filter_events_by_config_checkpoints(
    events,
    groups: list[GroupConfig],
    checkpoint_store: CheckpointStore,
):
    filtered = []
    for group in groups:
        matching = [
            event
            for event in events
            if event.group_name == group.display_name
            or event.group_id == group.slug
            or event.group_name in group.aliases
        ]
        filtered.extend(filter_new_events(matching, checkpoint_store.get(group.slug)))
    return sorted(filtered, key=lambda event: event.sent_at)


if __name__ == "__main__":
    raise SystemExit(main())
