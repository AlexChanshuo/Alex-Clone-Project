"""Personal LINE adapter contracts.

This module does not directly control LINE yet. It prepares deterministic
operation plans for the Computer Use executor so dangerous UI actions remain
observable and auditable.
"""

from __future__ import annotations

from dataclasses import dataclass


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

