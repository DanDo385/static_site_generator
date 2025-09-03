import unittest
from block_types import BlockType, block_to_block_type

class TestBlockTypes(unittest.TestCase):
    def test_paragraph_default(self):
        self.assertEqual(block_to_block_type("Just a normal line."),
                         BlockType.PARAGRAPH)

    def test_heading_levels_valid(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6"), BlockType.HEADING)

    def test_heading_requires_space(self):
        # No space after hashes -> not a heading per spec/course rule
        self.assertEqual(block_to_block_type("##Not a heading"),
                         BlockType.PARAGRAPH)

    def test_code_block_fenced(self):
        code = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_all_lines_prefixed(self):
        quote = ">\n> A wise line\n> Another"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_quote_must_be_every_line(self):
        mixed = ">\nNot quoted"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_unordered_list_hyphens(self):
        ul = "- apples\n- bananas\n- cherries"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_marker_fails(self):
        mixed = "- one\n* two"
        self.assertEqual(block_to_block_type(mixed), BlockType.PARAGRAPH)

    def test_ordered_list_sequential(self):
        ol = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_bad_sequence(self):
        bad = "1. one\n3. three"
        self.assertEqual(block_to_block_type(bad), BlockType.PARAGRAPH)

    def test_ordered_list_requires_space(self):
        bad = "1.one\n2. two"
        self.assertEqual(block_to_block_type(bad), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
