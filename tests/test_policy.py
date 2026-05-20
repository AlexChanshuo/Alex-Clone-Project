import unittest

from alex_clone.config import GroupConfig, PolicyConfig
from alex_clone.policy import build_reply_draft


class PolicyTests(unittest.TestCase):
    def test_unknown_group_drafts_only(self):
        policy = PolicyConfig(
            require_confirmation_for={"new_group"},
            allow_auto_send_for={"acknowledgement"},
        )
        draft = build_reply_draft("Unknown", "收到，我晚點看", None, policy)

        self.assertEqual(draft.policy_decision, "draft_only")

    def test_money_message_requires_confirmation(self):
        policy = PolicyConfig(
            require_confirmation_for={"money_or_contract"},
            allow_auto_send_for={"acknowledgement"},
        )
        draft = build_reply_draft("AI", "我會付款", approved_group(), policy)

        self.assertEqual(draft.risk_level, "high")
        self.assertEqual(draft.policy_decision, "ask_confirm")


def approved_group():
    return GroupConfig(
        display_name="AI",
        slug="ai",
        tags=["AI"],
        aliases=[],
        line_group_id="",
        status="approved",
        mode="draft_replies",
        allow_auto_send=False,
        daily_report=True,
        ingestion_adapter="line_personal_computer_use",
    )


if __name__ == "__main__":
    unittest.main()
