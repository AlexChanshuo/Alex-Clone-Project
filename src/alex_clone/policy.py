"""Outgoing action policy gate."""

from __future__ import annotations

from .config import GroupConfig, PolicyConfig
from .models import PolicyDecision, ReplyDraft, RiskLevel


HIGH_RISK_KEYWORDS = {
    "錢",
    "付款",
    "匯款",
    "合約",
    "報價",
    "承諾",
    "答應",
    "秘密",
    "個資",
    "地址",
    "電話",
}


def estimate_risk(text: str, calendar_checked: bool = False) -> RiskLevel:
    if any(keyword in text for keyword in HIGH_RISK_KEYWORDS):
        return "high"
    if any(keyword in text for keyword in ("時間", "開會", "約", "明天", "今天", "週", "下週")):
        return "medium" if calendar_checked else "high"
    return "low"


def decide_policy(
    text: str,
    group: GroupConfig | None,
    policy: PolicyConfig,
    intent: str = "reply",
    calendar_checked: bool = False,
) -> PolicyDecision:
    if group is None or group.status != "approved":
        return "blocked" if intent == "send" else "draft_only"

    risk = estimate_risk(text, calendar_checked=calendar_checked)
    if risk == "high":
        return "ask_confirm"
    if risk == "medium":
        return "ask_confirm"
    if intent in policy.allow_auto_send_for and group.allow_auto_send:
        return "auto_send_allowed"
    return "ask_confirm"


def build_reply_draft(
    target_group: str,
    text: str,
    group: GroupConfig | None,
    policy: PolicyConfig,
    target_person: str | None = None,
    source_reason: str = "manual command",
    intent: str = "reply",
    calendar_checked: bool = False,
) -> ReplyDraft:
    risk = estimate_risk(text, calendar_checked=calendar_checked)
    decision = decide_policy(
        text,
        group=group,
        policy=policy,
        intent=intent,
        calendar_checked=calendar_checked,
    )
    return ReplyDraft(
        target_group=target_group,
        target_person=target_person,
        source_reason=source_reason,
        draft_text=text,
        risk_level=risk,
        calendar_checked=calendar_checked,
        policy_decision=decision,
    )

