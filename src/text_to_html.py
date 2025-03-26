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
