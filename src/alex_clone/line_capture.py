"""Normalize personal LINE screen captures into LineEvent records."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config import GroupConfig
from .models import LineEvent


@dataclass(frozen=True)
class CapturedLineMessage:
    sender_name: str
    text: str
    sent_at: datetime | None = None
    message_id: str | None = None
    message_type: str = "text"
    confidence: float = 1.0
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class LineScreenCapture:
    group_title: str
    captured_at: datetime
    messages: list[CapturedLineMessage]
    source: str = "line_personal_computer_use"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LineScreenCapture":
        return cls(
            group_title=str(data["group_title"]),
            captured_at=parse_datetime(data.get("captured_at")),
            source=str(data.get("source", "line_personal_computer_use")),
            messages=[CapturedLineMessage(**normalize_message_payload(item)) for item in data.get("messages", [])],
        )


def read_capture(path: Path) -> LineScreenCapture:
    return LineScreenCapture.from_dict(json.loads(path.read_text(encoding="utf-8")))


def capture_to_events(capture: LineScreenCapture, group: GroupConfig) -> list[LineEvent]:
    validate_group_title(capture.group_title, group)
    events: list[LineEvent] = []
    for index, message in enumerate(capture.messages):
        sent_at = message.sent_at or capture.captured_at + timedelta(milliseconds=index)
        confidence = message.confidence if message.sent_at else min(message.confidence, 0.7)
        message_id = message.message_id or build_capture_message_id(group.slug, message, sent_at, index)
        metadata = dict(message.metadata or {})
        metadata.update(
            {
                "capture_group_title": capture.group_title,
                "capture_index": index,
                "timestamp_inferred": message.sent_at is None,
            }
        )
        events.append(
            LineEvent(
                source=capture.source,
                group_id=group.slug,
                group_name=group.display_name,
                message_id=message_id,
                sender_id=message.sender_name,
                sender_name=message.sender_name,
                sent_at=sent_at,
                type=message.message_type,
                text=message.text,
                confidence=confidence,
                metadata=metadata,
            )
        )
    return events


def validate_group_title(title: str, group: GroupConfig) -> None:
    normalized_title = normalize_title(title)
    allowed = {normalize_title(group.display_name), normalize_title(group.slug)}
    allowed.update(normalize_title(alias) for alias in group.aliases)
    if normalized_title not in allowed:
        raise ValueError(
            f"Capture title {title!r} does not match approved group {group.display_name!r} or aliases."
        )


def normalize_message_payload(item: dict[str, Any]) -> dict[str, Any]:
    sent_at = item.get("sent_at") or item.get("time")
    return {
        "sender_name": str(item.get("sender_name") or item.get("sender") or "Unknown Sender"),
        "text": str(item.get("text") or ""),
        "sent_at": parse_optional_datetime(sent_at),
        "message_id": item.get("message_id"),
        "message_type": str(item.get("type", "text")),
        "confidence": float(item.get("confidence", 1.0)),
        "metadata": dict(item.get("metadata", {})),
    }


def parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise ValueError("capture datetime is required")


def parse_optional_datetime(value: Any) -> datetime | None:
    if value in {None, ""}:
        return None
    return parse_datetime(value)


def build_capture_message_id(
    group_slug: str,
    message: CapturedLineMessage,
    sent_at: datetime,
    index: int,
) -> str:
    payload = "|".join(
        [
            group_slug,
            message.sender_name,
            sent_at.isoformat(),
            str(index),
            " ".join(message.text.split()),
        ]
    )
    return "capture-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def normalize_title(value: str) -> str:
    return "".join(value.casefold().split())

