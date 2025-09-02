import unittest
from textnode import TextNode, TextType
from textnode_to_htmlnode import text_node_to_html_node
from leafnode import LeafNode

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("Boldy", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Boldy")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("lean", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "lean")

    def test_code(self):
        node = TextNode("x += 1", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "x += 1")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})
        # Optional: end-to-end render
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://img.example/x.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # per spec: empty string
        self.assertEqual(
            html_node.props,
            {"src": "https://img.example/x.png", "alt": "Alt text"},
        )

    def test_link_missing_url_raises(self):
        node = TextNode("no url", TextType.LINK)  # url defaults to None
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_missing_url_raises(self):
        node = TextNode("no url", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_unsupported_type_raises(self):
        # Pass an invalid text_type to simulate a bad node
        bad = TextNode("oops", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(bad)

if __name__ == "__main__":
    unittest.main()
