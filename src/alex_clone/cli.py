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
from .io import events_to_jsonl, read_events_jsonl, write_events_jsonl
from .line_capture import capture_to_events, read_capture
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

    command_plan = subparsers.add_parser("command-plan", help="Turn a Telegram-style command into action targets.")
    command_plan.add_argument("text")
    command_plan.add_argument("--max-scrolls", type=int, default=6)
    command_plan.add_argument("--capture-limit", type=int, default=80)
    command_plan.set_defaults(func=cmd_command_plan)

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

    normalize_capture = subparsers.add_parser(
        "normalize-capture",
        help="Convert a LINE screen capture JSON file to normalized LineEvent JSONL.",
    )
    normalize_capture.add_argument("capture_json", type=Path)
    normalize_capture.add_argument("--group", required=True, help="Group display name, slug, or alias.")
    normalize_capture.add_argument("--output", type=Path, help="Optional JSONL output path.")
    normalize_capture.set_defaults(func=cmd_normalize_capture)

    ingest = subparsers.add_parser("ingest-manual", help="Append JSONL LINE events to alex-mind raw inbox.")
    ingest.add_argument("events_jsonl", type=Path)
    ingest.add_argument("--new-only", action="store_true", help="Skip events older than checkpoints.")
    ingest.add_argument("--update-checkpoint", action="store_true", help="Update group checkpoints after ingest.")
    ingest.set_defaults(func=cmd_ingest_manual)

    ingest_capture = subparsers.add_parser(
        "ingest-capture",
        help="Normalize and ingest a LINE screen capture JSON file.",
    )
    ingest_capture.add_argument("capture_json", type=Path)
    ingest_capture.add_argument("--group", required=True, help="Group display name, slug, or alias.")
    ingest_capture.add_argument("--new-only", action="store_true", help="Skip events older than checkpoints.")
    ingest_capture.add_argument("--update-checkpoint", action="store_true", default=True)
    ingest_capture.add_argument("--report", action="store_true", help="Print a daily report for ingested events.")
    ingest_capture.add_argument("--save-report", action="store_true", help="Save report/digest to alex-mind.")
    ingest_capture.set_defaults(func=cmd_ingest_capture)

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


def cmd_command_plan(args: argparse.Namespace, config) -> int:
    parsed = parse_command(args.text, config.groups)
    target_groups = resolve_groups_for_parsed_command(parsed, config.groups)
    checkpoint_store = CheckpointStore(config.state_dir)
    fetch_plans = []
    for group in target_groups:
        checkpoint = checkpoint_store.get(group.slug)
        plan = PersonalLineFetchPlan.from_group(
            group,
            checkpoint=checkpoint,
            max_scrolls=args.max_scrolls,
            capture_limit=args.capture_limit,
        )
        fetch_plans.append(
            {
                "group": group.display_name,
                "slug": group.slug,
                "tags": group.tags,
                "checkpoint": checkpoint_summary(checkpoint),
                "steps": plan.as_steps(),
            }
        )

    payload = {
        "parsed": parsed.__dict__,
        "target_groups": [group.display_name for group in target_groups],
        "fetch_plans": fetch_plans,
        "next_runtime_step": next_step_for_intent(parsed.intent),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if target_groups or parsed.intent in {"help", "list_groups"} else 2


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


def cmd_normalize_capture(args: argparse.Namespace, config) -> int:
    group = find_group(args.group, config.groups)
    if group is None or group.status != "approved":
        print(json.dumps({"error": "No approved group matched capture target."}, ensure_ascii=False, indent=2))
        return 2
    capture = read_capture(args.capture_json)
    events = capture_to_events(capture, group)
    if args.output:
        write_events_jsonl(args.output, events)
        print(json.dumps({"events": len(events), "output": str(args.output)}, ensure_ascii=False, indent=2))
    else:
        print(events_to_jsonl(events), end="")
    return 0


def cmd_ingest_manual(args: argparse.Namespace, config) -> int:
    events = read_events_jsonl(args.events_jsonl)
    result = ingest_events(
        events=events,
        config=config,
        new_only=args.new_only,
        update_checkpoint=args.update_checkpoint,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_ingest_capture(args: argparse.Namespace, config) -> int:
    group = find_group(args.group, config.groups)
    if group is None or group.status != "approved":
        print(json.dumps({"error": "No approved group matched capture target."}, ensure_ascii=False, indent=2))
        return 2
    events = capture_to_events(read_capture(args.capture_json), group)
    result = ingest_events(
        events=events,
        config=config,
        new_only=args.new_only,
        update_checkpoint=args.update_checkpoint,
    )
    if args.report or args.save_report:
        report_date = events[-1].sent_at.date() if events else date.today()
        markdown = generate_daily_report(events, report_date=report_date)
        if args.save_report:
            writer = VaultWriter(config.vault_dir)
            writer.ensure_ready()
            result["report_path"] = str(writer.write_daily_report(report_date, markdown))
            result["digest_path"] = str(writer.append_interaction_digest(report_date, markdown))
        if args.report:
            result["report_markdown"] = markdown
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def ingest_events(events, config, new_only: bool, update_checkpoint: bool):
    checkpoint_store = CheckpointStore(config.state_dir)
    if new_only:
        events = filter_events_by_config_checkpoints(events, config.groups, checkpoint_store)
    writer = VaultWriter(config.vault_dir)
    writer.ensure_ready()
    paths = [writer.append_raw_line_event(event) for event in events]
    unique_paths = sorted({str(path) for path in paths})
    updated_checkpoints = []
    if update_checkpoint:
        for group in groups_with_events(config.groups, events):
            checkpoint = checkpoint_store.update_from_events(group, events)
            updated_checkpoints.append({group.slug: checkpoint_summary(checkpoint)})
    return {
        "events_ingested": len(events),
        "ingested_event_dates": sorted({event.sent_at.date().isoformat() for event in events}),
        "paths": unique_paths,
        "updated_checkpoints": updated_checkpoints,
    }


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


def resolve_groups_for_parsed_command(parsed, groups: list[GroupConfig]) -> list[GroupConfig]:
    selected: list[GroupConfig] = []
    for group_name in parsed.group_matches:
        group = find_group(group_name, groups)
        if group and group.status == "approved" and group not in selected:
            selected.append(group)
    for tag in parsed.tags:
        for group in resolve_target_groups(None, tag, groups):
            if group not in selected:
                selected.append(group)
    return selected


def next_step_for_intent(intent: str) -> str:
    if intent in {"scan", "summarize"}:
        return "Execute fetch plan with Computer Use, then ingest-capture."
    if intent == "update_vault":
        return "Fetch or provide capture, then ingest-capture with --save-report."
    if intent == "draft_reply":
        return "Generate draft reply after fetching context; do not send without confirmation."
    if intent == "send_confirmed":
        return "Use personal-line-send-plan only for the already approved draft."
    if intent == "list_groups":
        return "Run groups command."
    if intent == "help":
        return "Run guide command."
    return "Ask Alex to clarify target tag/group and action."


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


def groups_with_events(groups: list[GroupConfig], events) -> list[GroupConfig]:
    selected = []
    for group in groups:
        group_names = {group.display_name, *group.aliases}
        if any(event.group_name in group_names or event.group_id == group.slug for event in events):
            selected.append(group)
    return selected


if __name__ == "__main__":
    raise SystemExit(main())
