"""Configuration loading for Alex Clone."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_VAULT_DIR = Path("/Users/alex/Documents/Alex-Clone/Alex-Mind")


@dataclass(frozen=True)
class GroupConfig:
    display_name: str
    slug: str
    line_group_id: str
    status: str
    mode: str
    allow_auto_send: bool
    daily_report: bool
    ingestion_adapter: str
    requires_active_group_title_check: bool = True


@dataclass(frozen=True)
class PolicyConfig:
    require_confirmation_for: set[str]
    allow_auto_send_for: set[str]


@dataclass(frozen=True)
class AppConfig:
    repo_root: Path
    vault_dir: Path
    groups: list[GroupConfig]
    policy: PolicyConfig


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_groups(path: Path) -> list[GroupConfig]:
    if not path.exists():
        return []
    data = load_json(path)
    groups = []
    for item in data.get("groups", []):
        groups.append(
            GroupConfig(
                display_name=item["display_name"],
                slug=item.get("slug") or slugify(item["display_name"]),
                line_group_id=item.get("line_group_id", ""),
                status=item.get("status", "pending_approval"),
                mode=item.get("mode", "observe_and_report"),
                allow_auto_send=bool(item.get("allow_auto_send", False)),
                daily_report=bool(item.get("daily_report", True)),
                ingestion_adapter=item.get("ingestion_adapter", "line_personal_computer_use"),
                requires_active_group_title_check=bool(
                    item.get("requires_active_group_title_check", True)
                ),
            )
        )
    return groups


def load_policy(path: Path) -> PolicyConfig:
    if not path.exists():
        return PolicyConfig(
            require_confirmation_for={
                "new_group",
                "calendar_create_or_edit",
                "sensitive_data",
                "money_or_contract",
                "emotional_or_ambiguous_reply",
                "cross_group_forwarding",
            },
            allow_auto_send_for={"acknowledgement", "received_will_review", "low_risk_logistics"},
        )
    data = load_json(path)
    return PolicyConfig(
        require_confirmation_for=set(data.get("require_confirmation_for", [])),
        allow_auto_send_for=set(data.get("allow_auto_send_for", [])),
    )


def load_config(repo_root: Path | None = None) -> AppConfig:
    root = repo_root or Path.cwd()
    vault_dir = Path(os.environ.get("ALEX_MIND_VAULT_DIR", DEFAULT_VAULT_DIR)).expanduser()
    groups_path = Path(os.environ.get("ALEX_CLONE_GROUPS_CONFIG", root / "config/groups.example.json"))
    policy_path = Path(os.environ.get("ALEX_CLONE_POLICY_CONFIG", root / "config/policy.example.json"))
    return AppConfig(
        repo_root=root,
        vault_dir=vault_dir,
        groups=load_groups(groups_path),
        policy=load_policy(policy_path),
    )


def slugify(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    parts = [part for part in normalized.split("-") if part]
    return "-".join(parts) or "unknown"

