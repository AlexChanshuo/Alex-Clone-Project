"""Input helpers for CLI workflows."""

from __future__ import annotations

import json
from pathlib import Path

from .models import LineEvent


def read_events_jsonl(path: Path) -> list[LineEvent]:
    events: list[LineEvent] = []
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                events.append(LineEvent.from_dict(json.loads(stripped)))
            except Exception as exc:  # noqa: BLE001 - CLI should report bad line context.
                raise ValueError(f"Invalid event at {path}:{line_number}: {exc}") from exc
    return events


def write_events_jsonl(path: Path, events: list[LineEvent]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event.to_json_dict(), ensure_ascii=False) + "\n")


def events_to_jsonl(events: list[LineEvent]) -> str:
    return "".join(json.dumps(event.to_json_dict(), ensure_ascii=False) + "\n" for event in events)
