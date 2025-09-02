# src/split_nodes_images_links.py
from textnode import TextNode, TextType
from markdown_extractors import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    """
    For each TextType.TEXT node, split the text on Markdown images:
      "before ![alt](url) after"
    -> [Text(TEXT, "before "), Text(IMAGE, alt, url), Text(TEXT, " after")]
    Non-TEXT nodes are passed through unchanged.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)  # list of (alt, url)
        if not matches:
            new_nodes.append(node)
            continue

        # Walk left-to-right, splitting by each literal image token once
        for alt, url in matches:
            token = f"![{alt}]({url})"
            before, sep, after = text.partition(token)  # split at first occurrence
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after  # continue with the remaining tail

        if text:  # trailing text (don't append empty text nodes)
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    For each TextType.TEXT node, split the text on Markdown links:
      "before [text](url) after"
    -> [Text(TEXT, "before "), Text(LINK, text, url), Text(TEXT, " after")]
    Non-TEXT nodes are passed through unchanged.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)  # list of (anchor, url)
        if not matches:
            new_nodes.append(node)
            continue

        for anchor, url in matches:
            token = f"[{anchor}]({url})"
            before, sep, after = text.partition(token)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
