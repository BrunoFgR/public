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

def extract_markdown_images(text):
    regex = r'!\[([^\]]*)\]\(([^)]*)\)'
    matches = re.findall(regex, text)
    return matches

def extract_markdown_links(text):
    regex = r'\[([^\]]*)\]\(([^)]*)\)'
    matches = re.findall(regex, text)
    return matches
