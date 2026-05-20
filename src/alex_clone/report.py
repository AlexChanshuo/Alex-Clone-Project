"""Daily report generation."""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from .models import LineEvent


QUESTION_MARKERS = ("?", "？", "嗎", "么", "請問")
TASK_MARKERS = ("幫", "需要", "記得", "todo", "待辦", "安排", "確認")


def generate_daily_report(events: list[LineEvent], report_date: date) -> str:
    grouped: dict[str, list[LineEvent]] = defaultdict(list)
    for event in events:
        grouped[event.group_name].append(event)

    lines = [
        "---",
        "type: alex-clone-daily-report",
        f"date: {report_date}",
        "source: alex-clone",
        "---",
        "",
        f"# Alex Clone Daily Report - {report_date}",
        "",
        "## Summary",
        f"- Groups reviewed: {len(grouped)}",
        f"- Messages captured: {len(events)}",
        "",
    ]

    if not events:
        lines.extend(["## Group Reports", "- No captured LINE events for this date.", ""])
        return "\n".join(lines)

    lines.append("## Group Reports")
    for group_name, group_events in sorted(grouped.items()):
        lines.extend(["", f"### {group_name}", ""])
        lines.append(f"- Messages: {len(group_events)}")
        important = select_important_messages(group_events)
        questions = [event for event in group_events if has_marker(event.text, QUESTION_MARKERS)]
        tasks = [event for event in group_events if has_marker(event.text, TASK_MARKERS)]

        lines.append("- Important updates:")
        for event in important:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not important:
            lines.append("  - None detected.")

        lines.append("- Questions for Alex:")
        for event in questions[:5]:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not questions:
            lines.append("  - None detected.")

        lines.append("- Tasks/open loops:")
        for event in tasks[:5]:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not tasks:
            lines.append("  - None detected.")

    lines.extend(
        [
            "",
            "## Suggested Reply Queue",
            "- Draft replies should be generated separately through the policy gate.",
            "",
            "## Vault Updates",
            "- Raw LINE events appended under `raw/inbox/line/`.",
            "- This report can be saved under `wiki/outputs/alex-clone-daily/`.",
        ]
    )
    return "\n".join(lines)


def select_important_messages(events: list[LineEvent]) -> list[LineEvent]:
    scored = sorted(events, key=lambda event: score_event(event), reverse=True)
    return [event for event in scored if score_event(event) > 0][:8]


def score_event(event: LineEvent) -> int:
    text = event.text.lower()
    score = 0
    for marker in ("決定", "重要", "提醒", "deadline", "會議", "活動", "報名", "付款"):
        if marker in text:
            score += 2
    if has_marker(event.text, QUESTION_MARKERS):
        score += 1
    if has_marker(event.text, TASK_MARKERS):
        score += 1
    if len(event.text) > 80:
        score += 1
    return score


def has_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in markers)


def compact(text: str, max_len: int = 180) -> str:
    one_line = " ".join(text.split())
    if len(one_line) <= max_len:
        return one_line
    return one_line[: max_len - 3] + "..."

