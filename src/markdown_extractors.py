# src/markdown_extractors.py
import re

# Images: ![alt](url)
_IMAGE_RE = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")

# Links (not images): [text](url) with negative lookbehind so "![...](...)" is excluded
_LINK_RE = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

def extract_markdown_images(text: str):
    """
    Return a list of (alt, url) tuples for Markdown images in `text`.
    Example: '![alt](https://example/img.png)' -> [('alt','https://example/img.png')]
    """
    return _IMAGE_RE.findall(text)

def extract_markdown_links(text: str):
    """
    Return a list of (text, url) tuples for Markdown links (excluding images).
    Example: '[Boot.dev](https://boot.dev)' -> [('Boot.dev','https://boot.dev')]
    """
    return _LINK_RE.findall(text)
