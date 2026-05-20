import unittest

from alex_clone.commands import parse_command
from alex_clone.config import GroupConfig


class CommandTests(unittest.TestCase):
    def test_scan_ai_group(self):
        parsed = parse_command("分身，去看 AI 群今天有什麼重要的", groups())

        self.assertEqual(parsed.intent, "scan")
        self.assertIn("AI", parsed.tags)

    def test_summarize_bni_group(self):
        parsed = parse_command("整理 BNI 今天重點並更新 alex-mind", groups())

        self.assertEqual(parsed.intent, "summarize")
        self.assertIn("BNI", parsed.tags)
        self.assertTrue(parsed.should_update_vault)

    def test_draft_reply_extracts_text(self):
        parsed = parse_command("幫我草擬回 AI 群：我晚點整理資料", groups())

        self.assertEqual(parsed.intent, "draft_reply")
        self.assertEqual(parsed.reply_text, "我晚點整理資料")

    def test_group_alias_match(self):
        parsed = parse_command("掃 BNI華AI名人堂分會 (43)", groups())

        self.assertIn("BNI華AI名人堂分會", parsed.group_matches)


def groups():
    return [
        GroupConfig(
            display_name="BNI華AI名人堂分會",
            slug="bni-ai-hall-of-fame",
            tags=["BNI"],
            aliases=["BNI華AI名人堂分會 (43)"],
            line_group_id="",
            status="approved",
            mode="observe_and_report",
            allow_auto_send=False,
            daily_report=True,
            ingestion_adapter="line_personal_computer_use",
        ),
        GroupConfig(
            display_name="AI實戰先鋒會 AI Agent group",
            slug="ai-agent-group",
            tags=["AI"],
            aliases=["AI實戰先鋒會"],
            line_group_id="",
            status="approved",
            mode="observe_and_report",
            allow_auto_send=False,
            daily_report=True,
            ingestion_adapter="line_personal_computer_use",
        ),
    ]


if __name__ == "__main__":
    unittest.main()

