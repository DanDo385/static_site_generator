# src/block_types.py
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    """
    Determine the Markdown block type for a single, trimmed block of text.
    Rules (per assignment):
      - Heading: 1–6 '#' then a space then text
      - Code: starts with ``` and ends with ```
      - Quote: every line starts with '>'
      - Unordered list: every line starts with '- '
      - Ordered list: each line starts with 'N. ' where N = 1..len(lines)
      - Otherwise: paragraph
    """
    # Code block: fenced with triple backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()

    # Heading (ATX): 1–6 hashes then a space then text, check the first line only
    if lines and re.match(r"^#{1,6} .+", lines[0]):
        return BlockType.HEADING

    # Quote: every line starts with '>'
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines must be "1. ", "2. ", ..., strictly increasing
    if lines:
        sequential = True
        for i, line in enumerate(lines, start=1):
            if not re.match(rf"^{i}\. .+", line):
                sequential = False
                break
        if sequential:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
