import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_simple(self):
        node = TextNode("This has a `code block` inside", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in new_nodes],
            [
                ("This has a ", TextType.TEXT),
                ("code block", TextType.CODE),
                (" inside", TextType.TEXT),
            ],
        )

    def test_bold_simple(self):
        node = TextNode("This **bold** word", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("This ", TextType.TEXT), ("bold", TextType.BOLD), (" word", TextType.TEXT)],
        )

    def test_italic_simple(self):
        node = TextNode("a _lean_ sentence", TextType.TEXT)
        out = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("a ", TextType.TEXT), ("lean", TextType.ITALIC), (" sentence", TextType.TEXT)],
        )

    def test_multiple_segments(self):
        node = TextNode("x **A** y **B** z", TextType.TEXT)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [
                ("x ", TextType.TEXT),
                ("A", TextType.BOLD),
                (" y ", TextType.TEXT),
                ("B", TextType.BOLD),
                (" z", TextType.TEXT),
            ],
        )

    def test_no_delimiter_kept_as_is(self):
        node = TextNode("just plain text", TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].text, "just plain text")
        self.assertEqual(out[0].text_type, TextType.TEXT)

    def test_non_text_nodes_unchanged(self):
        old = [
            TextNode("outside", TextType.TEXT),
            TextNode("boldy", TextType.BOLD),
            TextNode("tail", TextType.TEXT),
        ]
        out = split_nodes_delimiter(old, "**", TextType.BOLD)
        # The existing BOLD node should remain present and unmodified
        self.assertEqual([t.text_type for t in out], [TextType.TEXT, TextType.BOLD, TextType.TEXT])

    def test_unmatched_raises(self):
        node = TextNode("broken **bold here", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()
