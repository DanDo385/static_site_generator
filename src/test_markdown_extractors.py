import unittest
from markdown_extractors import extract_markdown_images, extract_markdown_links

class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_multiple(self):
        txt = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            extract_markdown_images(txt),
        )

    def test_extract_markdown_links_single(self):
        txt = "This is text with a link [to boot dev](https://www.boot.dev)"
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            extract_markdown_links(txt),
        )

    def test_extract_markdown_links_multiple(self):
        txt = "Links: [one](https://a.example) and [two](https://b.example/path?q=1)"
        self.assertListEqual(
            [
                ("one", "https://a.example"),
                ("two", "https://b.example/path?q=1"),
            ],
            extract_markdown_links(txt),
        )

    def test_links_do_not_capture_images(self):
        txt = "![pic](https://img.example/x.png) and [site](https://example.com)"
        self.assertListEqual(
            [("site", "https://example.com")],
            extract_markdown_links(txt),
        )

    def test_none_found(self):
        self.assertListEqual([], extract_markdown_links("no links here"))
        self.assertListEqual([], extract_markdown_images("no images here"))

if __name__ == "__main__":
    unittest.main()
