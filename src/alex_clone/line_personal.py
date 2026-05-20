"""Personal LINE adapter contracts.

This module does not directly control LINE yet. It prepares deterministic
operation plans for the Computer Use executor so dangerous UI actions remain
observable and auditable.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import GroupConfig
from .models import FetchCheckpoint


@dataclass(frozen=True)
class PersonalLineSendPlan:
    target_group: str
    message: str
    require_title_check: bool = True
    require_clipboard_paste: bool = True
    require_screenshot_on_stuck: bool = True
    require_send_audit: bool = True

    def as_steps(self) -> list[str]:
        return [
            "Open Alex's personal LINE desktop/web session on this Mac.",
            f"Search or select the approved group: {self.target_group}",
            "Verify the active group title exactly matches the target group.",
            "Paste the prepared message from clipboard.",
            "Stop before send unless the policy gate says send is confirmed.",
            "After send, write an audit record with message hash and proof path.",
        ]


@dataclass(frozen=True)
class PersonalLineFetchPlan:
    target_group: str
    group_slug: str
    tags: list[str]
    aliases: list[str]
    last_seen_at: str | None
    last_event_fingerprint: str | None
    max_scrolls: int = 6
    capture_limit: int = 80
    require_title_check: bool = True
    require_checkpoint_stop: bool = True
    require_screenshot_on_stuck: bool = True

    @classmethod
    def from_group(
        cls,
        group: GroupConfig,
        checkpoint: FetchCheckpoint | None = None,
        max_scrolls: int = 6,
        capture_limit: int = 80,
    ) -> "PersonalLineFetchPlan":
        return cls(
            target_group=group.display_name,
            group_slug=group.slug,
            tags=group.tags,
            aliases=group.aliases,
            last_seen_at=checkpoint.last_seen_at.isoformat() if checkpoint and checkpoint.last_seen_at else None,
            last_event_fingerprint=checkpoint.last_event_fingerprint if checkpoint else None,
            max_scrolls=max_scrolls,
            capture_limit=capture_limit,
        )

    def as_steps(self) -> list[str]:
        stop_rule = "Stop when the checkpoint message is found."
        if not self.last_event_fingerprint:
            stop_rule = "No checkpoint yet; capture the most recent visible history within limits."
        return [
            "Open Alex's personal LINE desktop/web session on this Mac.",
            f"Search or select the approved group: {self.target_group}",
            "Verify the active group title matches the display name or one alias.",
            "Capture visible message bubbles with sender, timestamp if visible, and text.",
            f"Scroll upward up to {self.max_scrolls} times, staying in the same group.",
            stop_rule,
            f"Do not capture more than {self.capture_limit} messages in one run.",
            "Normalize captures into LineEvent JSONL.",
            "Write raw events to alex-mind and update the checkpoint only after successful ingest.",
            "Return a short summary to Telegram/Codex with captured count and any uncertainty.",
        ]
