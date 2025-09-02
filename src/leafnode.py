# src/leafnode.py

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # children are not allowed for a LeafNode
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        # All leaf nodes must have a value
        if self.value is None:
            raise ValueError("LeafNode must have a value.")

        # Raw text node when tag is None
        if self.tag is None:
            return self.value

        # Render with tag + optional props
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
