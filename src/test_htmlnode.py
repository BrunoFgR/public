import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            {},
        )

    def test_leaf_values(self):
        leaf = LeafNode(None, "This is a text")
        self.assertEqual(leaf.value, "This is a text")
        self.assertEqual(leaf.props, {})
        self.assertIsNone(leaf.tag)

    def test_leaf_to_html(self):
        leaf = LeafNode("span", "This is a text")
        self.assertEqual(leaf.to_html(), "<span>This is a text</span>")

    def test_leaf_without_tag(self):
        leaf = LeafNode(None, "This is a text")
        self.assertEqual(leaf.to_html(), "This is a text")

    def test_leaf_to_html_a(self):
        leaf = LeafNode("a", "This is a link", {"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">This is a link</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_attributes(self):
        child_node = LeafNode("span", "child", {"class": "child"})
        parent_node = ParentNode("div", [child_node], {"id": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent"><span class="child">child</span></div>',
        )

    def test_to_html_with_many_children(self):
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag='p', value='What a strange world', children=None, props={'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()
