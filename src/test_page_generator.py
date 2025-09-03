import unittest
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_ignores_h2_and_uses_first_h1(self):
        md = """## Not the title
# Real Title
Some text...
"""
        self.assertEqual(extract_title(md), "Real Title")

    def test_h1_with_extra_spaces(self):
        self.assertEqual(extract_title("#    Spaced   "), "Spaced")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("No headings here\n## sub only\nparagraph")

if __name__ == "__main__":
    unittest.main()
