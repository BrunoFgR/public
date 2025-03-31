import unittest
from gencontent import extract_title

class TestGenContext(unittest.TestCase):
    def test_basic_title(self):
        """Test a simple title at the beginning of the string."""
        markdown = "# My Title\nSome content here"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_content_before(self):
        """Test a title that has content before it."""
        markdown = "Some intro text\n# My Title\nSome content here"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_with_special_characters(self):
        """Test a title with special characters."""
        markdown = "# My Title: With! Special? Characters*"
        self.assertEqual(extract_title(markdown), "My Title: With! Special? Characters*")

    def test_title_with_markdown_formatting(self):
        """Test a title with markdown formatting inside."""
        markdown = "# My *Italic* and **Bold** Title"
        self.assertEqual(extract_title(markdown), "My *Italic* and **Bold** Title")

    def test_title_with_links(self):
        """Test a title containing a markdown link."""
        markdown = "# Title with [link](https://example.com)"
        self.assertEqual(extract_title(markdown), "Title with [link](https://example.com)")

    def test_multiple_titles_returns_first(self):
        """Test that only the first title is extracted when there are multiple."""
        markdown = "# First Title\nContent\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_title_with_multiple_spaces(self):
        """Test a title with multiple spaces after the hash."""
        markdown = "#    My Title with extra spaces"
        self.assertEqual(extract_title(markdown), "My Title with extra spaces")

    def test_empty_title_text(self):
        """Test an empty title text."""
        markdown = "# "
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_no_title_raises_error(self):
        """Test that an error is raised when no title is found."""
        markdown = "Content without a title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_incorrect_title_format_raises_error(self):
        """Test that an error is raised when title format is incorrect."""
        markdown = "#Incorrect title format (no space after #)"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_higher_level_heading_not_matched(self):
        """Test that higher level headings (##, ###) are not matched."""
        markdown = "## Second level heading\n# First level heading"
        self.assertEqual(extract_title(markdown), "First level heading")

    def test_empty_string(self):
        """Test with an empty string."""
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
