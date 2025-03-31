import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType
)
from htmlnode import HTMLNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a simple paragraph with text."
        expected = ["This is a simple paragraph with text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        expected = ["First paragraph.", "Second paragraph.", "Third paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_newlines(self):
        markdown = "\n\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_with_whitespace(self):
        markdown = "  Paragraph with spaces  \n\n  Another with spaces  "
        expected = ["Paragraph with spaces", "Another with spaces"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_headings_and_paragraphs(self):
        markdown = "# Heading\n\nParagraph below heading.\n\n## Subheading"
        expected = ["# Heading", "Paragraph below heading.", "## Subheading"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_code_blocks(self):
        markdown = "Regular text.\n\n```\ncode block\nwith multiple lines\n```\n\nMore text."
        expected = ["Regular text.", "```\ncode block\nwith multiple lines\n```", "More text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_lists(self):
        markdown = "- Item 1\n- Item 2\n\n1. First\n2. Second"
        expected = ["- Item 1\n- Item 2", "1. First\n2. Second"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_blockquotes(self):
        markdown = ">This is a quote\n>More of the quote\n\nRegular paragraph"
        expected = [">This is a quote\n>More of the quote", "Regular paragraph"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_newlines(self):
        markdown = "\n\nFirst block.\n\nSecond block.\n\n"
        expected = ["First block.", "Second block."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```python\ndef hello():\n    print('hello')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
        # Test invalid unordered list (mixed content)
        self.assertEqual(block_to_block_type("- Item 1\nNot a list item"), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)
        # Test invalid ordered list (numbers out of sequence)
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 3"), BlockType.PARAGRAPH)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2\n> Line 3"), BlockType.QUOTE)
        # Test invalid quote (mixed content)
        self.assertEqual(block_to_block_type("> Line 1\nNot a quote"), BlockType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Paragraph line 1\nParagraph line 2"), BlockType.PARAGRAPH)
        # Test that other formats not matching criteria are paragraphs
        self.assertEqual(block_to_block_type("#Not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a list - with dash"), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def assert_html_equal(self, node, expected_html):
        """Helper method to compare generated HTML with expected output"""
        self.assertEqual(node.to_html(), expected_html)

    def test_empty_markdown(self):
        """Test that empty markdown produces an empty div"""
        html_node = markdown_to_html_node("")
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 0)

    def test_single_paragraph(self):
        """Test a single paragraph conversion"""
        markdown = "This is a simple paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "p")
        self.assert_html_equal(html_node, "<div><p>This is a simple paragraph.</p></div>")

    def test_multiple_paragraphs(self):
        """Test conversion of multiple paragraphs"""
        markdown = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 3)
        self.assert_html_equal(html_node,
            "<div><p>First paragraph.</p><p>Second paragraph.</p><p>Third paragraph.</p></div>")

    def test_headings(self):
        """Test conversion of different heading levels"""
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[1].tag, "h2")
        self.assertEqual(html_node.children[2].tag, "h3")
        self.assert_html_equal(html_node,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>")

    def test_code_blocks(self):
        """Test conversion of code blocks"""
        markdown = "```\nfunction test() {\n  return true;\n}\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "pre")
        self.assert_html_equal(html_node,
            "<div><pre><code>function test() {\n  return true;\n}\n</code></pre></div>")

    def test_unordered_lists(self):
        """Test conversion of unordered lists"""
        markdown = "- Item 1\n- Item 2\n- Item 3"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ul")
        self.assertEqual(len(html_node.children[0].children), 3)
        self.assert_html_equal(html_node,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_ordered_lists(self):
        """Test conversion of ordered lists"""
        markdown = "1. First item\n2. Second item\n3. Third item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "ol")
        self.assertEqual(len(html_node.children[0].children), 3)
        self.assert_html_equal(html_node,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>")

    def test_blockquotes(self):
        """Test conversion of blockquotes"""
        markdown = "> This is a quote\n> It spans multiple lines"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.children[0].tag, "blockquote")
        self.assert_html_equal(html_node,
            "<div><blockquote>This is a quote It spans multiple lines</blockquote></div>")

    def test_inline_formatting(self):
        """Test conversion with inline formatting elements"""
        markdown = "This has **bold** and _italic_ text, and `code` too."
        html_node = markdown_to_html_node(markdown)
        self.assert_html_equal(html_node,
            "<div><p>This has <b>bold</b> and <i>italic</i> text, and <code>code</code> too.</p></div>")
