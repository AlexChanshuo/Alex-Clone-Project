import unittest
from datetime import date
from pathlib import Path

from alex_clone.io import read_events_jsonl
from alex_clone.report import generate_daily_report


class ReportTests(unittest.TestCase):
    def test_generate_daily_report_detects_questions_and_tasks(self):
        events = read_events_jsonl(Path("tests/fixtures/line_events.jsonl"))
        report = generate_daily_report(events, date(2026, 5, 20))

        self.assertIn("AI實戰先鋒會 AI Agent group", report)
        self.assertIn("Questions for Alex", report)
        self.assertIn("Kevin", report)
        self.assertIn("Tasks/open loops", report)


if __name__ == "__main__":
    unittest.main()

