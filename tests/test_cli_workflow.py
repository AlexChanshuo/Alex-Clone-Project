import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from alex_clone.cli import main


class CliWorkflowTests(unittest.TestCase):
    def test_command_plan_resolves_ai_tag(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = run_cli(
                [
                    "--repo-root",
                    ".",
                    "command-plan",
                    "分身，去看 AI 群今天有什麼重要的",
                ],
                state_dir=Path(tmp),
            )

        payload = json.loads(output)
        self.assertIn("AI實戰先鋒會 AI Agent group", payload["target_groups"])
        self.assertEqual(payload["parsed"]["intent"], "scan")

    def test_normalize_capture_outputs_jsonl(self):
        output = run_cli(
            [
                "--repo-root",
                ".",
                "normalize-capture",
                "tests/fixtures/line_capture_ai.json",
                "--group",
                "AI實戰先鋒會",
            ]
        )

        lines = [json.loads(line) for line in output.splitlines()]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["group_id"], "ai-agent-group")

    def test_ingest_capture_updates_only_matching_checkpoint(self):
        with tempfile.TemporaryDirectory() as state_tmp, tempfile.TemporaryDirectory() as vault_tmp:
            output = run_cli(
                [
                    "--repo-root",
                    ".",
                    "ingest-capture",
                    "tests/fixtures/line_capture_ai.json",
                    "--group",
                    "AI實戰先鋒會",
                    "--new-only",
                    "--update-checkpoint",
                ],
                state_dir=Path(state_tmp),
                vault_dir=Path(vault_tmp),
            )

        payload = json.loads(output)
        self.assertEqual(payload["events_ingested"], 2)
        self.assertEqual(len(payload["updated_checkpoints"]), 1)
        self.assertIn("ai-agent-group", payload["updated_checkpoints"][0])


def run_cli(args, state_dir: Path | None = None, vault_dir: Path | None = None):
    buffer = io.StringIO()
    old_env = {}
    import os

    if state_dir is not None:
        old_env["ALEX_CLONE_STATE_DIR"] = os.environ.get("ALEX_CLONE_STATE_DIR")
        os.environ["ALEX_CLONE_STATE_DIR"] = str(state_dir)
    if vault_dir is not None:
        old_env["ALEX_MIND_VAULT_DIR"] = os.environ.get("ALEX_MIND_VAULT_DIR")
        os.environ["ALEX_MIND_VAULT_DIR"] = str(vault_dir)
    try:
        with redirect_stdout(buffer):
            exit_code = main(args)
    finally:
        for key, previous in old_env.items():
            if previous is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous
    assert exit_code == 0
    return buffer.getvalue()


if __name__ == "__main__":
    unittest.main()
