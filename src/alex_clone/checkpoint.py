"""Checkpoint storage for personal LINE fetches."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from .config import GroupConfig
from .models import FetchCheckpoint, LineEvent
from .vault import utcish_now


class CheckpointStore:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.path = state_dir / "line-checkpoints.json"

    def load_all(self) -> dict[str, FetchCheckpoint]:
        if not self.path.exists():
            return {}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            slug: FetchCheckpoint.from_dict(payload)
            for slug, payload in data.get("checkpoints", {}).items()
        }

    def get(self, group_slug: str) -> FetchCheckpoint | None:
        return self.load_all().get(group_slug)

    def save(self, checkpoint: FetchCheckpoint) -> None:
        checkpoints = self.load_all()
        checkpoints[checkpoint.group_slug] = checkpoint
        self.state_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "checkpoints": {
                slug: item.to_json_dict()
                for slug, item in sorted(checkpoints.items())
            }
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.path.chmod(0o600)

    def update_from_events(self, group: GroupConfig, events: list[LineEvent]) -> FetchCheckpoint:
        group_names = {group.display_name, *group.aliases}
        group_events = [
            event
            for event in events
            if event.group_name in group_names or event.group_id == group.slug
        ]
        if not group_events:
            existing = self.get(group.slug)
            if existing:
                return existing
            checkpoint = FetchCheckpoint(
                group_slug=group.slug,
                last_event_fingerprint=None,
                last_seen_at=None,
                updated_at=utcish_now(),
            )
            self.save(checkpoint)
            return checkpoint

        latest = max(group_events, key=lambda event: event.sent_at)
        checkpoint = FetchCheckpoint(
            group_slug=group.slug,
            last_event_fingerprint=event_fingerprint(latest),
            last_seen_at=latest.sent_at,
            updated_at=utcish_now(),
        )
        self.save(checkpoint)
        return checkpoint


def event_fingerprint(event: LineEvent) -> str:
    payload = "|".join(
        [
            event.group_id,
            event.group_name,
            event.sender_name,
            event.sent_at.isoformat(),
            " ".join(event.text.split()),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def filter_new_events(events: list[LineEvent], checkpoint: FetchCheckpoint | None) -> list[LineEvent]:
    if checkpoint is None:
        return events
    new_events: list[LineEvent] = []
    for event in sorted(events, key=lambda item: item.sent_at):
        if checkpoint.last_seen_at and event.sent_at <= checkpoint.last_seen_at:
            continue
        if checkpoint.last_event_fingerprint and event_fingerprint(event) == checkpoint.last_event_fingerprint:
            continue
        new_events.append(event)
    return new_events


def checkpoint_summary(checkpoint: FetchCheckpoint | None) -> dict[str, str | None]:
    if checkpoint is None:
        return {
            "last_event_fingerprint": None,
            "last_seen_at": None,
            "updated_at": None,
        }
    return {
        "last_event_fingerprint": checkpoint.last_event_fingerprint,
        "last_seen_at": checkpoint.last_seen_at.isoformat() if checkpoint.last_seen_at else None,
        "updated_at": checkpoint.updated_at.isoformat(),
    }
