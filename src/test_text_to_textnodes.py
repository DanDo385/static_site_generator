import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_example_from_assignment(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(result, expected)

    def test_plain_text(self):
        text = "Just plain text with no markdown"
        result = text_to_textnodes(text)
        expected = [TextNode("Just plain text with no markdown", TextType.TEXT)]
        self.assertListEqual(result, expected)

    def test_bold_only(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_italic_only(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_code_only(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_image_only(self):
        text = "This is an ![image](https://example.com/img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertListEqual(result, expected)

    def test_link_only(self):
        text = "This is a [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(result, expected)

    def test_multiple_bold(self):
        text = "**First** and **second** bold"
        result = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_multiple_italic(self):
        text = "_First_ and _second_ italic"
        result = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.ITALIC),
            TextNode(" italic", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_multiple_code(self):
        text = "`First` and `second` code"
        result = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_complex_combination(self):
        text = "**Bold** _italic_ `code` ![img](url) [link](url) text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(result, expected)

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        expected = [TextNode("", TextType.TEXT)]
        self.assertListEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
