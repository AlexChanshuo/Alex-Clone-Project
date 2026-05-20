import unittest

from alex_clone.config import normalize_tags


class ConfigTests(unittest.TestCase):
    def test_normalize_tags_removes_blank_and_duplicate_values(self):
        self.assertEqual(normalize_tags(["AI", " ", "AI", "BNI"]), ["AI", "BNI"])


if __name__ == "__main__":
    unittest.main()

