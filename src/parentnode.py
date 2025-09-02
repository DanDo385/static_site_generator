from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """
    A parent HTML node: must have a tag and children, no direct value.
    props is optional.
    """
    def __init__(self, tag, children, props=None):
        # value is always None for a parent node
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        # treat missing/empty children as an error per spec
        if not self.children:
            raise ValueError("ParentNode must have children.")
        rendered = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{rendered}</{self.tag}>"
