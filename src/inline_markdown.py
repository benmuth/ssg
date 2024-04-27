from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_bold,
    text_type_image,
    text_type_link,
)

import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if not isinstance(old_node, TextNode):
            nodes.append(old_node)
            continue

        parts = old_node.text_node.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown: unmatched delimiter")

        for i in range(len(parts)):
            if not parts[i]:
                continue

            if i % 2 == 0:
                nodes.append(TextNode(parts[i], old_node.text_type))
            else:
                nodes.append(TextNode(parts[i], text_type))
    return nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_node:
            continue
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        image_tuples = extract_markdown_images(node.text_node)

        # no images in node, just append
        if not image_tuples:
            new_nodes.append(node)
            continue
        
        tup = image_tuples[0]
        splits = node.text_node.split(f"![{tup[0]}]({tup[1]})", 1)
       
        if splits[0]:
            first_text_node = TextNode(splits[0], text_type_text)
            new_nodes.append(first_text_node)

        image_node = TextNode(tup[0], text_type_image, tup[1])
        new_nodes.append(image_node)

        new_nodes.extend(split_nodes_image([TextNode(splits[1], text_type_text)]))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text_node:
            continue
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        link_tuples = extract_markdown_links(node.text_node)

        # no links in node, just append
        if not link_tuples:
            new_nodes.append(node)
            continue
        
        tup = link_tuples[0]
        splits = node.text_node.split(f"[{tup[0]}]({tup[1]})", 1)
       
        if splits[0]:
            first_text_node = TextNode(splits[0], text_type_text)
            new_nodes.append(first_text_node)

        link_node = TextNode(tup[0], text_type_link, tup[1])
        new_nodes.append(link_node)

        new_nodes.extend(split_nodes_link([TextNode(splits[1], text_type_text)]))

    return new_nodes


def extract_markdown_images(text):
    md_img_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(md_img_regex, text)


def extract_markdown_links(text):
    md_link_regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(md_link_regex, text)

def text_to_text_nodes(text):
    text_nodes = [TextNode(text, text_type_text)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
    
    
