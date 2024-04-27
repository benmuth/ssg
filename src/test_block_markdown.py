import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_bold,
    text_type_image,
    text_type_link,
)

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)

from block_markdown import markdown_to_blocks, markdown_to_html_node

from pprint import pprint

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        input = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        got = markdown_to_blocks(input)

        want = [
            "This is **bolded** paragraph",
            """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
            """* This is a list
* with items""",
        ]

        self.assertEqual(got, want)

    def test_markdown_to_blocks_single(self):
        input = """This is **bolded** paragraph
"""

        got = markdown_to_blocks(input)

        want = ["This is **bolded** paragraph\n"]

        self.assertEqual(got, want)



class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html(self):
        input = """## Features

Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
AngularJS-powered HTML5 Markdown editor.

- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML to Markdown converter
- [jQuery] - duh

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible.

```sh
gulp build dist --prod
```

1. harder
2. better
3. faster
4. stronger"""
        node = markdown_to_html_node(input)
        pprint(node)
        # print(node.tag)
        # print(node.children[0])
        self.assertEqual(node.children[0].tag, "h2")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")
        self.assertEqual(node.children[3].tag, "blockquote")
        self.assertEqual(node.children[4].tag, "blockquote")
        self.assertEqual(node.children[5].tag, "pre")
        self.assertEqual(node.children[6].tag, "ol")

