from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text_node, text_type, url=None):
        self.text_node = text_node
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text_node == other.text_node
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text_node}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(value=text_node.text_node)
    elif text_node.text_type == text_type_bold:
        return LeafNode(value=text_node.text_node, tag = "b")
    elif text_node.text_type == text_type_italic:
        return LeafNode(value=text_node.text_node, tag = "i")
    elif text_node.text_type == text_type_code:
        return LeafNode(value=text_node.text_node, tag = "code")
    elif text_node.text_type == text_type_link:
        return LeafNode(value=text_node.text_node, tag = "a", props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode(value="", tag = "img", props={"src": text_node.url, "alt": text_node.text_node})
    else:
        raise Exception("invalid type for text node")


