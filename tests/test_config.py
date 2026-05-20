import tempfile
import unittest
from pathlib import Path

from alex_clone.config import load_env_file, normalize_tags


class ConfigTests(unittest.TestCase):
    def test_normalize_tags_removes_blank_and_duplicate_values(self):
        self.assertEqual(normalize_tags(["AI", " ", "AI", "BNI"]), ["AI", "BNI"])

    def test_load_env_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".env"
            path.write_text("A=1\n# comment\nB='two'\n", encoding="utf-8")

            self.assertEqual(load_env_file(path), {"A": "1", "B": "two"})


if __name__ == "__main__":
    unittest.main()
