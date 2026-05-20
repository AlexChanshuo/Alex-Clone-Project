import unittest
from pathlib import Path


class HermesScaffoldTests(unittest.TestCase):
    def test_hermes_agent_files_exist(self):
        root = Path("hermes/alexma-clone")
        for relative in [
            "SOUL.md",
            "USER.md",
            "MEMORY.md",
            "AGENTS.md",
            "skills/alex-clone-line/SKILL.md",
            "skills/alex-clone-line/references/cli.md",
        ]:
            self.assertTrue((root / relative).exists(), relative)

    def test_skill_mentions_deterministic_cli(self):
        skill = Path("hermes/alexma-clone/skills/alex-clone-line/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("alex_clone.cli command-plan", skill)
        self.assertIn("ingest-capture", skill)
        self.assertIn("Do not directly write vault files", skill)


if __name__ == "__main__":
    unittest.main()

