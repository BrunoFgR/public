import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode):
    match (text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", None, {"href": text_node.url, "alt": text_node.text})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = []
        section = old_node.text.split(delimiter)
        if len(section) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(section)):
            if section[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(section[i], TextType.TEXT))
            else:
                split_node.append(TextNode(section[i], text_type))
        new_nodes.extend(split_node)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        check_for_unclosed_images(original_text)
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        check_for_unclosed_links(original_text)
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    regex = r'!\[([^\]]*)\]\(([^)]*)\)'
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches

def check_for_unclosed_links(text):
    # First, look for properly formatted links
    proper_links_pattern = r'\[([^\]]*)\]\(([^)]*)\)'

    # Then, look for patterns that started like a link but weren't properly closed
    unclosed_patterns = [
        r'\[([^\]]*)\]\([^)]*$',     # Unclosed URL parenthesis
        r'\[([^\]]*)\($',            # Started URL but no closing parenthesis
        r'\[([^\]]*)$',              # Unclosed text bracket
    ]

    # Remove all properly formatted links from the text
    cleaned_text = re.sub(proper_links_pattern, '', text)

    # Check if any unclosed patterns remain
    for pattern in unclosed_patterns:
        if re.search(pattern, cleaned_text):
            raise ValueError(f"Invalid markdown: link not properly closed. Found unclosed pattern matching: {pattern}")

    return True

def check_for_unclosed_images(text):
    # Pattern for properly formatted images
    proper_image_pattern = r'!\[([^\]]*)\]\(([^)]*)\)'

    # Remove all properly formatted images from the text
    cleaned_text = re.sub(proper_image_pattern, '', text)

    # Patterns for unclosed image elements
    unclosed_image_patterns = [
        r'!\[([^\]]*)\]\([^)]*$',     # Unclosed URL parenthesis in image
        r'!\[([^\]]*)\($',            # Started URL but no closing parenthesis in image
        r'!\[([^\]]*)$',              # Unclosed alt text bracket in image
    ]

    # Check if any unclosed image patterns remain
    for pattern in unclosed_image_patterns:
        if re.search(pattern, cleaned_text):
            raise ValueError("Invalid markdown: unclosed image element found")

    return True
