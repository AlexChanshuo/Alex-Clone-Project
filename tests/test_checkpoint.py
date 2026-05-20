import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from alex_clone.checkpoint import CheckpointStore, event_fingerprint, filter_new_events
from alex_clone.config import GroupConfig
from alex_clone.models import LineEvent


class CheckpointTests(unittest.TestCase):
    def test_update_and_filter_events(self):
        group = approved_group()
        old = event("m1", "2026-05-20T09:00:00+08:00", "old")
        new = event("m2", "2026-05-20T10:00:00+08:00", "new")

        with tempfile.TemporaryDirectory() as tmp:
            store = CheckpointStore(Path(tmp))
            checkpoint = store.update_from_events(group, [old])

            self.assertEqual(checkpoint.last_event_fingerprint, event_fingerprint(old))
            self.assertEqual(filter_new_events([old, new], checkpoint), [new])

    def test_alias_group_updates_checkpoint(self):
        group = approved_group()
        alias_event = event("m1", "2026-05-20T09:00:00+08:00", "hello", group_name="AI實戰先鋒會")

        with tempfile.TemporaryDirectory() as tmp:
            store = CheckpointStore(Path(tmp))
            checkpoint = store.update_from_events(group, [alias_event])

            self.assertIsNotNone(checkpoint.last_event_fingerprint)


def approved_group():
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


def event(message_id, sent_at, text, group_name="AI實戰先鋒會 AI Agent group"):
    return LineEvent(
        source="line_personal_computer_use",
        group_id="ai-agent-group",
        group_name=group_name,
        message_id=message_id,
        sender_id="u1",
        sender_name="Alex",
        sent_at=datetime.fromisoformat(sent_at),
        type="text",
        text=text,
    )


if __name__ == "__main__":
    unittest.main()

