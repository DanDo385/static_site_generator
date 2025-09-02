import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "This is a single paragraph with no breaks."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no breaks."])

    def test_multiple_blocks(self):
        md = """# Heading 1

This is paragraph 1.

This is paragraph 2.

- List item 1
- List item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "This is paragraph 1.",
                "This is paragraph 2.",
                "- List item 1\n- List item 2",
            ],
        )

    def test_empty_blocks_filtered(self):
        md = """First block


Second block

Third block"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block",
                "Second block",
                "Third block",
            ],
        )

    def test_whitespace_stripped(self):
        md = """   First block with leading spaces   

   Second block with trailing spaces   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with leading spaces",
                "Second block with trailing spaces",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_heading_and_paragraph(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            ],
        )

    def test_list_block(self):
        md = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_mixed_content(self):
        md = """# Heading

Paragraph with **bold** and _italic_.

- List item 1
- List item 2

Another paragraph.

## Subheading

Final paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph with **bold** and _italic_.",
                "- List item 1\n- List item 2",
                "Another paragraph.",
                "## Subheading",
                "Final paragraph.",
            ],
        )

if __name__ == "__main__":
    unittest.main()
