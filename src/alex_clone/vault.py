"""alex-mind vault writer."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from .config import slugify
from .models import LineEvent, SendAudit


class VaultWriter:
    def __init__(self, vault_dir: Path) -> None:
        self.vault_dir = vault_dir

    def ensure_ready(self) -> None:
        self.vault_dir.mkdir(parents=True, exist_ok=True)

    def append_raw_line_event(self, event: LineEvent) -> Path:
        day = event.sent_at.date().isoformat()
        group_slug = slugify(event.group_name)
        path = self.vault_dir / "raw" / "inbox" / "line" / day / f"{group_slug}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event.to_json_dict(), ensure_ascii=False) + "\n")
        return path

    def write_daily_report(self, report_date: date, markdown: str) -> Path:
        path = self.vault_dir / "wiki" / "outputs" / "alex-clone-daily" / f"{report_date}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")
        return path

    def append_interaction_digest(self, report_date: date, markdown: str) -> Path:
        path = (
            self.vault_dir
            / "wiki"
            / "syntheses"
            / "interactions-rolling"
            / f"{report_date}-line-digest.md"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write("\n\n")
            file.write(markdown.rstrip())
            file.write("\n")
        return path

    def append_send_audit(self, audit: SendAudit) -> Path:
        day = audit.timestamp.date().isoformat()
        path = self.vault_dir / "logs" / "line-send-audit" / f"{day}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": audit.timestamp.isoformat(),
            "target_group": audit.target_group,
            "command": audit.command,
            "message_hash": audit.message_hash,
            "policy_decision": audit.policy_decision,
            "confirmation_required": audit.confirmation_required,
            "proof_path": audit.proof_path,
        }
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return path


def utcish_now() -> datetime:
    return datetime.now().astimezone()

