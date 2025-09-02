import unittest
from textnode import TextNode, TextType
from split_nodes_images_links import split_nodes_image, split_nodes_link

class TestSplitNodesImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_basic(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_no_images_returns_original(self):
        node = TextNode("no pics here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_no_links_returns_original(self):
        node = TextNode("no links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_nodes_unchanged(self):
        old = [
            TextNode("plain", TextType.TEXT),
            TextNode("already a link", TextType.LINK, "https://x.example"),
            TextNode("tail", TextType.TEXT),
        ]
        out = split_nodes_link(old)
        self.assertEqual(out[1].text_type, TextType.LINK)
        self.assertEqual(out[1].url, "https://x.example")

    def test_image_then_link_separate_calls(self):
        # Demonstrates sequential application: images first, then links
        node = TextNode(
            "![pic](https://img.example/x.png) and [site](https://example.com)",
            TextType.TEXT,
        )
        after_images = split_nodes_image([node])
        # now split links in the result
        final_nodes = split_nodes_link(after_images)
        self.assertListEqual(
            [
                TextNode("pic", TextType.IMAGE, "https://img.example/x.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://example.com"),
            ],
            final_nodes,
        )

if __name__ == "__main__":
    unittest.main()
