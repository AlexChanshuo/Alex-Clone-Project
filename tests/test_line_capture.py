import unittest
from pathlib import Path

from alex_clone.config import GroupConfig
from alex_clone.line_capture import capture_to_events, read_capture, validate_group_title


class LineCaptureTests(unittest.TestCase):
    def test_capture_to_events_uses_alias_and_infers_missing_timestamp(self):
        capture = read_capture(Path("tests/fixtures/line_capture_ai.json"))
        events = capture_to_events(capture, group())

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].group_name, "AI實戰先鋒會 AI Agent group")
        self.assertFalse(events[0].metadata["timestamp_inferred"])
        self.assertTrue(events[1].metadata["timestamp_inferred"])
        self.assertLess(events[1].confidence, 1.0)

    def test_validate_group_title_rejects_wrong_group(self):
        with self.assertRaises(ValueError):
            validate_group_title("Wrong Group", group())


def group():
    return GroupConfig(
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
    )


if __name__ == "__main__":
    unittest.main()

