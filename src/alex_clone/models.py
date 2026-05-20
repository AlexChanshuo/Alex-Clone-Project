"""Core data models for Alex Clone."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal


EventType = Literal["text", "image", "file", "system", "unknown"]
RiskLevel = Literal["low", "medium", "high"]
PolicyDecision = Literal["draft_only", "ask_confirm", "auto_send_allowed", "blocked"]


@dataclass(frozen=True)
class LineEvent:
    """Normalized LINE event captured from personal LINE, webhook, or import."""

    source: str
    group_id: str
    group_name: str
    message_id: str
    sender_id: str
    sender_name: str
    sent_at: datetime
    type: EventType
    text: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LineEvent":
        sent_at_raw = data.get("sent_at")
        if isinstance(sent_at_raw, datetime):
            sent_at = sent_at_raw
        elif isinstance(sent_at_raw, str):
            sent_at = datetime.fromisoformat(sent_at_raw)
        else:
            raise ValueError("LineEvent.sent_at is required")

        return cls(
            source=str(data.get("source", "manual_import")),
            group_id=str(data.get("group_id") or data.get("group_name") or "unknown-group"),
            group_name=str(data.get("group_name") or data.get("group_id") or "Unknown Group"),
            message_id=str(data.get("message_id") or f"manual-{int(sent_at.timestamp())}"),
            sender_id=str(data.get("sender_id") or data.get("sender_name") or "unknown-sender"),
            sender_name=str(data.get("sender_name") or data.get("sender_id") or "Unknown Sender"),
            sent_at=sent_at,
            type=data.get("type", "text"),
            text=str(data.get("text", "")),
            confidence=float(data.get("confidence", 1.0)),
            metadata=dict(data.get("metadata", {})),
        )

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "group_id": self.group_id,
            "group_name": self.group_name,
            "message_id": self.message_id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "sent_at": self.sent_at.isoformat(),
            "type": self.type,
            "text": self.text,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class ReplyDraft:
    target_group: str
    target_person: str | None
    source_reason: str
    draft_text: str
    risk_level: RiskLevel
    calendar_checked: bool
    policy_decision: PolicyDecision


@dataclass(frozen=True)
class SendAudit:
    timestamp: datetime
    target_group: str
    command: str
    message_hash: str
    policy_decision: PolicyDecision
    confirmation_required: bool
    proof_path: str | None = None

