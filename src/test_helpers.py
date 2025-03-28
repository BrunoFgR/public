import unittest
from textnode import TextNode, TextType
from helpers import (
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links
)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props["href"], "https://www.boot.dev")
        self.assertEqual(html_node.props["alt"], "This is a text node")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://www.boot.dev")
        self.assertEqual(html_node.props["alt"], "This is a text node")

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestMarkdownImagesExtraction(unittest.TestCase):
    def test_no_images(self):
        """Test with text containing no markdown images."""
        text = "This is a plain text with no images."
        self.assertEqual(extract_markdown_images(text), [])

    def test_single_image(self):
        """Test with a single markdown image."""
        text = "Here is an image: ![alt text](image.jpg)"
        expected = [("alt text", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        """Test with multiple markdown images."""
        text = """
        # Document with Images

        ![First image](first.png)
        Some text here
        ![Second image](second.jpg)
        """
        expected = [("First image", "first.png"), ("Second image", "second.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_empty_alt_text(self):
        """Test with empty alt text."""
        text = "Image with no alt text: ![](empty_alt.png)"
        expected = [("", "empty_alt.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_images_with_urls(self):
        """Test with images that have URLs as sources."""
        text = """
        ![Remote image](https://example.com/image.jpg)
        ![Another remote](http://test.org/pic.png)
        """
        expected = [
            ("Remote image", "https://example.com/image.jpg"),
            ("Another remote", "http://test.org/pic.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_images_with_paths(self):
        """Test with images that have file paths."""
        text = """
        ![Local image](/path/to/image.jpg)
        ![Relative image](../images/pic.png)
        """
        expected = [
            ("Local image", "/path/to/image.jpg"),
            ("Relative image", "../images/pic.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_mixed_content(self):
        """Test with mixed markdown content including images."""
        text = """
        # Title

        Some paragraph with text.

        ![Image in content](image.png)

        * List item 1
        * List item 2 with ![inline image](inline.jpg)

        [Link text](https://example.com)
        """
        expected = [
            ("Image in content", "image.png"),
            ("inline image", "inline.jpg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_special_characters(self):
        """Test with special characters in alt text and URLs."""
        text = """
        ![Image with spaces and symbols: !@#$%](file with spaces.jpg)
        ![Another's "special" image](path/to/file-name_123.png)
        """
        expected = [
            ("Image with spaces and symbols: !@#$%", "file with spaces.jpg"),
            ("Another's \"special\" image", "path/to/file-name_123.png")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

class TestMarkdownLinkExtraction(unittest.TestCase):
    def test_empty_string(self):
        """Test with an empty string - should return empty list."""
        self.assertEqual(extract_markdown_links(""), [])

    def test_no_links(self):
        """Test with text that has no links."""
        text = "This is a plain text with no links."
        self.assertEqual(extract_markdown_links(text), [])

    def test_single_link(self):
        """Test with text containing a single link."""
        text = "Here is a [link](https://example.com)."
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        """Test with text containing multiple links."""
        text = "Check [first link](https://example.com) and [second link](https://another-example.org)."
        expected = [
            ("first link", "https://example.com"),
            ("second link", "https://another-example.org")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_links_with_special_characters(self):
        """Test with links containing special characters."""
        text = "Special chars in [text with-symbols!](https://example.com/path?query=value#fragment)"
        expected = [("text with-symbols!", "https://example.com/path?query=value#fragment")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        """Test with an empty link text."""
        text = "This is an [](https://example.com) empty link text."
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_url(self):
        """Test with an empty URL."""
        text = "This is a [link with empty URL]()."
        expected = [("link with empty URL", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_nested_brackets(self):
        """Test with nested brackets in link text."""
        text = "This is a [[nested] bracket](https://example.com) link."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiline_text(self):
        """Test with links spread across multiple lines."""
        text = """Line 1 with [link1](url1)
                 Line 2 with [link2](url2)"""
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_code_formatting(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_italic_formatting(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_bold_formatting(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_link_formatting(self):
        text = "This is a [link](https://example.com) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_image_formatting(self):
        text = "This is an ![image](image.jpg) text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "image.jpg")
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multiple_formatting(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")


    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 0)

    def test_invalid_markdown(self):
        # Test unclosed code section
        with self.assertRaises(ValueError):
            text_to_textnodes("This is `unclosed code")

        # Test unclosed italic section
        with self.assertRaises(ValueError):
            text_to_textnodes("This is _unclosed italic")

        # Test unclosed bold section
        with self.assertRaises(ValueError):
            text_to_textnodes("This is **unclosed bold")

        # Test invalid link
        with self.assertRaises(ValueError):
            text_to_textnodes("This is [unclosed](link")

        # Test invalid image
        with self.assertRaises(ValueError):
            text_to_textnodes("This is ![unclosed](image")
