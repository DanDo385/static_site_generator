import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grand = LeafNode("b", "grandchild")
        child = ParentNode("span", [grand])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_props_on_parent(self):
        child = LeafNode(None, "hi")
        parent = ParentNode("p", [child], props={"class": "greeting"})
        self.assertEqual(parent.to_html(), '<p class="greeting">hi</p>')

    def test_missing_tag_raises(self):
        child = LeafNode("i", "x")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

if __name__ == "__main__":
    unittest.main()
