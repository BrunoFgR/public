import unittest
from block_markdown import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs_with_extra_newlines(self):
        md = """First paragraph.


        Second paragraph.



        Third paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph.",
                "Second paragraph.",
                "Third paragraph.",
            ],
        )

    def test_headings_and_paragraphs(self):
        md = """# Heading 1

        ## Heading 2

        Paragraph text here.

        ### Heading 3
        Directly followed text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1",
                "## Heading 2",
                "Paragraph text here.",
                "### Heading 3\nDirectly followed text.",
            ],
        )

    def test_code_blocks(self):
        md = """Regular paragraph.

        ```python
        def hello_world():
            print("Hello, world!")
        ```

        Text after code block."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular paragraph.",
                "```python\ndef hello_world():\nprint(\"Hello, world!\")\n```",
                "Text after code block.",
            ],
        )

    def test_blockquotes(self):
        md = """Regular text.

        > This is a blockquote
        > It continues here

        More text."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Regular text.",
                "> This is a blockquote\n> It continues here",
                "More text.",
            ],
        )

    def test_complex_nested_structure(self):
        md = """# Main Title

        Introduction paragraph with **bold** and _italic_ text.

        ## Section 1

        - List item 1
        - List item 2
          - Nested item

        ```
        Code block here
        More code
        ```

        > Blockquote
        > More quote

        Final paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Title",
                "Introduction paragraph with **bold** and _italic_ text.",
                "## Section 1",
                "- List item 1\n- List item 2\n- Nested item",
                "```\nCode block here\nMore code\n```",
                "> Blockquote\n> More quote",
                "Final paragraph.",
            ],
        )

    def test_only_whitespace(self):
        md = """



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_horizontal_rules(self):
        md = """Paragraph 1

        ---

        Paragraph 2

        ***

        Paragraph 3"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph 1",
                "---",
                "Paragraph 2",
                "***",
                "Paragraph 3",
            ],
        )
