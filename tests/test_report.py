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
        self.assertIn("可能需要 Alex 回覆", report)
        self.assertIn("Kevin", report)
        self.assertIn("待辦 / open loops", report)

    def test_generate_daily_report_detects_test_requests_and_acknowledgements(self):
        events = read_events_jsonl(Path("tests/fixtures/line_events_report_requests.jsonl"))
        report = generate_daily_report(events, date(2026, 5, 21))

        self.assertIn("新版模型部署完成", report)
        self.assertIn("請測試一下", report)
        self.assertIn("稍晚測試並回覆", report)
        self.assertNotIn("None detected", report)


if __name__ == "__main__":
    unittest.main()
