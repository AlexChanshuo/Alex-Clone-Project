"""Natural-language command interpretation for Alex Clone."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .config import GroupConfig


Intent = Literal[
    "scan",
    "summarize",
    "update_vault",
    "draft_reply",
    "send_confirmed",
    "list_groups",
    "help",
    "unknown",
]


TAG_ALIASES: dict[str, set[str]] = {
    "BNI": {"bni", "商會", "分會", "華ai", "華 ai", "名人堂", "palms", "引薦"},
    "AI": {"ai", "人工智慧", "agent", "代理", "工具", "科技", "模型"},
    "family": {"family", "家人", "家庭", "爸", "媽", "老婆", "小孩", "親戚"},
    "Friends": {"friends", "friend", "朋友", "好友", "聚會", "社交"},
}

INTENT_KEYWORDS: dict[Intent, set[str]] = {
    "scan": {
        "掃",
        "掃描",
        "看",
        "查看",
        "檢查",
        "巡",
        "巡一下",
        "讀",
        "抓",
        "fetch",
        "scan",
        "check",
        "watch",
        "monitor",
        "看看",
    },
    "summarize": {
        "整理",
        "總結",
        "摘要",
        "重點",
        "懶人包",
        "報告",
        "summary",
        "summarize",
        "digest",
        "brief",
    },
    "update_vault": {
        "更新vault",
        "更新 vault",
        "寫進vault",
        "寫進 vault",
        "存到vault",
        "存到 vault",
        "更新alex-mind",
        "更新 alex-mind",
        "記到腦袋",
        "存記憶",
        "update vault",
        "save memory",
    },
    "draft_reply": {
        "草擬",
        "擬回",
        "幫我回",
        "幫我寫",
        "回覆草稿",
        "draft",
        "reply draft",
        "write reply",
    },
    "send_confirmed": {
        "確認送出",
        "送出",
        "發出去",
        "可以發",
        "confirm",
        "send it",
        "send",
    },
    "list_groups": {
        "群組列表",
        "有哪些群",
        "watchlist",
        "list groups",
        "groups",
        "tag列表",
        "標籤列表",
    },
    "help": {
        "help",
        "指令",
        "怎麼用",
        "教我",
        "用法",
        "guide",
        "指南",
    },
}


@dataclass(frozen=True)
class ParsedCommand:
    raw_text: str
    intent: Intent
    tags: list[str] = field(default_factory=list)
    group_matches: list[str] = field(default_factory=list)
    reply_text: str | None = None
    should_update_vault: bool = False
    confidence: float = 0.0


def parse_command(text: str, groups: list[GroupConfig]) -> ParsedCommand:
    normalized = normalize_text(text)
    intent = detect_intent(normalized)
    tags = detect_tags(normalized)
    group_matches = detect_groups(normalized, groups)
    should_update_vault = detect_intent(normalized, only="update_vault") == "update_vault"
    reply_text = extract_reply_text(text) if intent in {"draft_reply", "send_confirmed"} else None
    confidence = score_confidence(intent, tags, group_matches, should_update_vault)

    return ParsedCommand(
        raw_text=text,
        intent=intent,
        tags=tags,
        group_matches=group_matches,
        reply_text=reply_text,
        should_update_vault=should_update_vault,
        confidence=confidence,
    )


def detect_intent(normalized_text: str, only: Intent | None = None) -> Intent:
    intents = [only] if only else [
        "send_confirmed",
        "draft_reply",
        "summarize",
        "scan",
        "update_vault",
        "list_groups",
        "help",
    ]
    for intent in intents:
        if intent is None:
            continue
        for keyword in INTENT_KEYWORDS[intent]:
            if normalize_text(keyword) in normalized_text:
                return intent
    return "unknown"


def detect_tags(normalized_text: str) -> list[str]:
    tags: list[str] = []
    for tag, aliases in TAG_ALIASES.items():
        candidates = {tag, *aliases}
        if any(normalize_text(candidate) in normalized_text for candidate in candidates):
            tags.append(tag)
    return tags


def detect_groups(normalized_text: str, groups: list[GroupConfig]) -> list[str]:
    matches: list[str] = []
    for group in groups:
        candidates = [group.display_name, group.slug, *group.aliases]
        if any(normalize_text(candidate) in normalized_text for candidate in candidates):
            matches.append(group.display_name)
    return matches


def extract_reply_text(text: str) -> str | None:
    separators = ["：", ":", "說", "回覆", "message"]
    for separator in separators:
        if separator in text:
            candidate = text.split(separator, 1)[1].strip()
            return candidate or None
    return None


def normalize_text(text: str) -> str:
    return "".join(text.casefold().split())


def score_confidence(
    intent: Intent,
    tags: list[str],
    group_matches: list[str],
    should_update_vault: bool,
) -> float:
    score = 0.0
    if intent != "unknown":
        score += 0.45
    if tags:
        score += 0.25
    if group_matches:
        score += 0.25
    if should_update_vault:
        score += 0.05
    return min(score, 1.0)


def command_guidance() -> str:
    return "\n".join(
        [
            "你可以這樣叫 Alex 分身：",
            "- 掃 AI 群",
            "- 看 BNI 今天有什麼重要的",
            "- 整理 Friends 群重點",
            "- 檢查 family 有沒有需要我回",
            "- 更新 alex-mind，把今天 AI 群重點存起來",
            "- 幫我草擬回 AI 群：我晚點整理資料",
            "- 確認送出",
            "- 群組列表 / groups",
        ]
    )

