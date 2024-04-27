import pprint
from htmlnode import ParentNode, LeafNode, HTMLNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    return markdown.split("\n\n")


def block_to_block_type(block):
    start = block.split()[0]
    end = block.split()[-1]

    if "#" in start:
        count = start.count("#")
        if count <= 6:
            return block_type_heading

    if start[:3] == "```" and end == "```":
        return block_type_code

    lines = block.split("\n")
    if all([line.startswith(">") for line in lines]):
        return block_type_quote

    if all([line.startswith("* ") or line.startswith("- ") for line in lines]):
        return block_type_unordered_list

    if lines[0].startswith("1. "):
        is_ordered_list = False
        count = 1
        for line in lines:
            prefix = line.split(".")[0]
            is_ordered_list = prefix == str(count)
            count += 1
        if is_ordered_list:
            return block_type_ordered_list

    return block_type_paragraph


def paragraph_to_html_node(block):
    return LeafNode(tag="p", value=block)
    # return "<p>" + block + "</p>"


def heading_to_html_node(block):
    start = block.split()[0]
    count = start.count("#")
    return LeafNode(tag=f"h{count}", value=block[count + 1 :])


def code_to_html_node(block):
    trimmed_block = block[:3][3:]
    inner = LeafNode(value=trimmed_block, tag="code")
    return ParentNode(children=[inner], tag="pre")


def quote_to_html_node(block):
    break_block = block.replace("\n>", "<br>")
    return LeafNode(tag="blockquote", value=break_block)


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        items.append(LeafNode(tag="li", value=line.lstrip("-* ")))
    return ParentNode(children=items, tag="ul")


def ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        items.append(LeafNode(tag="li", value=line.split(". ", maxsplit=1)[1]))

    return ParentNode(children=items, tag="ol")


def markdown_to_html_node(markdown):
    parent_node = ParentNode([], "div")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if not block:
            continue
        type = block_to_block_type(block)

        block_node = None

        if type == block_type_paragraph:
            block_node = paragraph_to_html_node(block)
        elif type == block_type_heading:
            block_node = heading_to_html_node(block)
        elif type == block_type_code:
            block_node = code_to_html_node(block)
        elif type == block_type_quote:
            block_node = quote_to_html_node(block)
        elif type == block_type_unordered_list:
            block_node = unordered_list_to_html_node(block)
        elif type == block_type_ordered_list:
            block_node = ordered_list_to_html_node(block)

        if not block_node:
            raise ValueError("unknown block type")

        if block_node.value:
            children_text_nodes = text_to_text_nodes(block_node.value)
            children_html_nodes = []
            for node in children_text_nodes:
                children_html_nodes.append(text_node_to_html_node(node))

            # if len(children_html_nodes) > 1:
            block_node = ParentNode(children=children_html_nodes, tag=block_node.tag, props=block_node.props)
                # block_node.children = children_html_nodes
        parent_node.children.append(block_node)
    return parent_node
