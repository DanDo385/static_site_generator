# src/split_nodes.py
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextType.TEXT nodes on the given delimiter, alternating:
      outside -> TextType.TEXT
      inside  -> text_type (e.g., TextType.CODE, BOLD, ITALIC)

    Raises:
      ValueError if there is an unmatched delimiter.
    """
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes; keep other types as-is
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)  # e.g. "a `b` c" -> ["a ", "b", " c"]
        if len(parts) == 1:
            # No delimiter present; keep the node unchanged
            new_nodes.append(node)
            continue

        # If there isn't a matching closing delimiter, there will be an even number of parts
        # e.g., "a `b" -> ["a ", "b"] -> len(parts) == 2 (even) => error
        if len(parts) % 2 == 0:
            raise ValueError(
                f"Unmatched delimiter '{delimiter}' in text: {node.text!r}"
            )

        # Build nodes: even indices are outside (TEXT), odd indices are inside (text_type)
        for i, chunk in enumerate(parts):
            if i % 2 == 0:
                # Outside the delimiters -> plain text
                if chunk:
                    new_nodes.append(TextNode(chunk, TextType.TEXT))
            else:
                # Inside the delimiters -> the provided text_type
                new_nodes.append(TextNode(chunk, text_type))

    return new_nodes
