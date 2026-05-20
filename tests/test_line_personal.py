import unittest

from alex_clone.config import GroupConfig
from alex_clone.line_personal import PersonalLineFetchPlan


class LinePersonalTests(unittest.TestCase):
    def test_fetch_plan_steps_include_title_check_and_checkpoint(self):
        plan = PersonalLineFetchPlan.from_group(group())
        steps = "\n".join(plan.as_steps())

        self.assertIn("Verify the active group title", steps)
        self.assertIn("No checkpoint yet", steps)
        self.assertEqual(plan.group_slug, "ai-agent-group")


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

