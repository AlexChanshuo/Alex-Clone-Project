"""Daily report generation."""

from __future__ import annotations

from collections import defaultdict
from datetime import date

from .models import LineEvent


QUESTION_MARKERS = ("?", "？", "嗎", "么", "請問", "可不可以", "能不能", "是否", "有沒有")
REQUEST_MARKERS = (
    "請",
    "麻煩",
    "幫",
    "需要",
    "記得",
    "確認",
    "測試",
    "看一下",
    "回覆",
    "處理",
    "安排",
    "提醒",
    "todo",
    "待辦",
)
IMPORTANT_MARKERS = (
    "決定",
    "重要",
    "提醒",
    "deadline",
    "會議",
    "活動",
    "報名",
    "付款",
    "部署",
    "上線",
    "更新",
    "完成",
    "問題",
    "失敗",
    "錯誤",
    "urgent",
)
ACK_MARKERS = ("收到", "了解", "ok", "okay", "晚點", "稍晚", "我會", "我來")


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
        f"# Alex Clone 每日 LINE 摘要 - {report_date}",
        "",
        "## 總覽",
        f"- 已檢查群組：{len(grouped)}",
        f"- 擷取訊息：{len(events)}",
        "",
    ]

    if not events:
        lines.extend(["## 群組摘要", "- 今天沒有擷取到 LINE 訊息。", ""])
        return "\n".join(lines)

    lines.append("## 群組摘要")
    for group_name, group_events in sorted(grouped.items()):
        lines.extend(["", f"### {group_name}", ""])
        lines.append(f"- 訊息數：{len(group_events)}")
        important = select_important_messages(group_events)
        questions = [event for event in group_events if has_marker(event.text, QUESTION_MARKERS)]
        tasks = [event for event in group_events if has_marker(event.text, REQUEST_MARKERS)]
        acknowledgements = [event for event in group_events if has_marker(event.text, ACK_MARKERS)]

        lines.append("- 要注意的重點：")
        for event in important:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not important:
            lines.append("  - 沒有明顯重點。")

        lines.append("- 可能需要 Alex 回覆：")
        for event in questions[:5]:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not questions:
            lines.append("  - 沒有明顯問題。")

        lines.append("- 待辦 / open loops：")
        for event in tasks[:5]:
            lines.append(f"  - {event.sender_name}: {compact(event.text)}")
        if not tasks:
            lines.append("  - 沒有明顯待辦。")

        if acknowledgements:
            lines.append("- 已有人承接 / 回應：")
            for event in acknowledgements[:5]:
                lines.append(f"  - {event.sender_name}: {compact(event.text)}")

    lines.extend(
        [
            "",
            "## 建議回覆佇列",
            "- 需要送出的回覆應另外用 policy gate 產生草稿，不在報告裡直接送出。",
            "",
            "## Vault 更新",
            "- Raw LINE events 已追加到 `raw/inbox/line/`。",
            "- 此報告可儲存到 `wiki/outputs/alex-clone-daily/`。",
        ]
    )
    return "\n".join(lines)


def select_important_messages(events: list[LineEvent]) -> list[LineEvent]:
    scored = sorted(events, key=lambda event: score_event(event), reverse=True)
    return [event for event in scored if score_event(event) > 0][:8]


def score_event(event: LineEvent) -> int:
    text = event.text.lower()
    score = 0
    for marker in IMPORTANT_MARKERS:
        if marker in text:
            score += 2
    if has_marker(event.text, QUESTION_MARKERS):
        score += 1
    if has_marker(event.text, REQUEST_MARKERS):
        score += 1
    if has_marker(event.text, ACK_MARKERS):
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
