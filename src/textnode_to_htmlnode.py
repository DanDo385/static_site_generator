# src/textnode_to_htmlnode.py
from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """
    Convert a TextNode (Markdown-ish inline content) into a LeafNode (HTML).
    Raises ValueError for unsupported types or missing required data.
    """
    t = text_node.text_type

    if t == TextType.TEXT:
        # raw text (no tag)
        return LeafNode(None, text_node.text)

    if t == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if t == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if t == TextType.CODE:
        return LeafNode("code", text_node.text)

    if t == TextType.LINK:
        if not text_node.url:
            raise ValueError("LINK TextNode requires a url")
        # <a href="...">anchor text</a>
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if t == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("IMAGE TextNode requires a url")
        # <img src="..." alt="..."> as a LeafNode with empty value
        # (LeafNode renders open+close tags; acceptable for our assignment)
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    # Anything else: error
    raise ValueError(f"Unsupported TextType: {t}")
