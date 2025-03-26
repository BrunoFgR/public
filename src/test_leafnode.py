import unittest
from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_values(self):
        leaf = LeafNode(value="This is a text")
        self.assertEqual(leaf.value, "This is a text")
        self.assertEqual(leaf.props, {})
        self.assertIsNone(leaf.tag)

    def test_to_html(self):
        leaf = LeafNode("span", "This is a text")
        leaf2 = LeafNode(value="This is another text")
        self.assertEqual(leaf.to_html(), "<span>This is a text</span>")
        self.assertEqual(leaf2.to_html(), "<>This is another text</>")

    def test_leaf_to_html_a(self):
        leaf = LeafNode("a", "This is a link", {"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">This is a link</a>')
