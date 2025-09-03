# src/markdown_to_html.py
import re
from htmlnode import HTMLNode  # base
from parentnode import ParentNode
from leafnode import LeafNode
from block_types import BlockType, block_to_block_type

# Inline helpers you already built
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter
from split_nodes_images_links import split_nodes_image, split_nodes_link
from textnode_to_htmlnode import text_node_to_html_node

# --- Small utility: split raw markdown into blocks (blank-line separated)
def _split_blocks(md: str):
    # normalize newlines; split on one or more blank lines; drop empty blocks
    blocks = [b.strip() for b in re.split(r"\n\s*\n", md.strip()) if b.strip()]
    return blocks

# --- Turn inline markdown text into a list of HTML LeafNodes
def _text_to_children(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    # handle images & links first so they don't get split by other passes
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # then code, bold, italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # convert TextNode -> LeafNode
    return [text_node_to_html_node(n) for n in nodes]

# --- Block renderers
def _render_heading(block: str):
    m = re.match(r"^(#{1,6}) (.+)$", block)
    hashes, text = m.group(1), m.group(2)
    tag = f"h{len(hashes)}"
    return ParentNode(tag, _text_to_children(text))

def _render_code(block: str):
    # Fence on its own line, content between; keep a trailing newline inside <code>
    lines = block.splitlines()
    inner = "\n".join(lines[1:-1])
    if not inner.endswith("\n"):
        inner += "\n"
    code = LeafNode("code", inner)
    return ParentNode("pre", [code])

def _render_quote(block: str):
    # Strip a single leading '>' and optional space per line, keep line breaks
    stripped_lines = [re.sub(r"^>\s?", "", ln) for ln in block.splitlines()]
    text = "\n".join(stripped_lines)
    return ParentNode("blockquote", _text_to_children(text))

def _render_ul(block: str):
    items = []
    for ln in block.splitlines():
        # each line starts with "- " by prior classification
        content = ln[2:]
        items.append(ParentNode("li", _text_to_children(content)))
    return ParentNode("ul", items)

def _render_ol(block: str):
    items = []
    for ln in block.splitlines():
        # remove leading "N. "
        content = re.sub(r"^\d+\.\s+", "", ln)
        items.append(ParentNode("li", _text_to_children(content)))
    return ParentNode("ol", items)

def _render_paragraph(block: str):
    # collapse internal newlines to spaces (matches the example expectation)
    text = " ".join(block.splitlines())
    return ParentNode("p", _text_to_children(text))

# --- Main entry point
def markdown_to_html_node(markdown: str) -> HTMLNode:
    block_nodes = []
    for block in _split_blocks(markdown):
        btype = block_to_block_type(block)
        if btype == BlockType.HEADING:
            block_nodes.append(_render_heading(block))
        elif btype == BlockType.CODE:
            block_nodes.append(_render_code(block))
        elif btype == BlockType.QUOTE:
            block_nodes.append(_render_quote(block))
        elif btype == BlockType.UNORDERED_LIST:
            block_nodes.append(_render_ul(block))
        elif btype == BlockType.ORDERED_LIST:
            block_nodes.append(_render_ol(block))
        else:
            block_nodes.append(_render_paragraph(block))
    # Wrap all blocks in a <div>
    return ParentNode("div", block_nodes)
