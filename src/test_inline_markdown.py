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


class TestSplitNode(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_bold_multiple(self):
        node = TextNode("This **text** has **multiple** delimiters!", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" has ", text_type_text),
            TextNode("multiple", text_type_bold),
            TextNode(" delimiters!", text_type_text),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_bold_complex(self):
        node = TextNode(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
            text_type_text,
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(
                " with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
                text_type_text,
            ),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_italics(self):
        node = TextNode("This *is fancy*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
            TextNode("This ", text_type_text),
            TextNode("is fancy", text_type_italic),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_italic_start(self):
        node = TextNode("*Fancy* is this", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected = [
            TextNode("Fancy", text_type_italic),
            TextNode(" is this", text_type_text),
        ]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])


class TestExtract(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        got = extract_markdown_images(text)
        want = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]

        self.assertEqual(got, want)

    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"

        got = extract_markdown_links(text)
        want = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(got, want)

    def test_extract_none(self):
        text = "This is just text"

        got = extract_markdown_links(text)
        want = []
        self.assertEqual(got, want)


class TestSplitLinks(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) link!",
            text_type_text,
        )
        got = split_nodes_link([node])

        want = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" link!", text_type_text),
        ]
        self.assertEqual(got, want)

    def test_split_link_end(self):
        node = TextNode(
            "This is text with a [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        got = split_nodes_link([node])

        want = [
            TextNode("This is text with a ", text_type_text),
            TextNode(
                "link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(got, want)

    def test_split_link_start(self):
        node = TextNode(
            "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        got = split_nodes_link([node])

        want = [
            TextNode(
                "link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second link",
                text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(got, want)

    def test_split_link_none(self):
        node = TextNode(
            "This is text",
            text_type_text,
        )

        got = split_nodes_link([node])

        want = [TextNode("This is text", text_type_text)]
        self.assertEqual(got, want)


class TestSplitImages(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) image!",
            text_type_text,
        )

        got = split_nodes_image([node])

        want = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" image!", text_type_text),
        ]
        self.assertEqual(got, want)

    def test_split_image_start(self):
        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) image!",
            text_type_text,
        )

        got = split_nodes_image([node])

        want = [
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
            TextNode(" image!", text_type_text),
        ]
        self.assertEqual(got, want)

    def test_split_image_end(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )

        got = split_nodes_image([node])

        want = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(got, want)

    def test_split_image_none(self):
        node = TextNode(
            "This is text",
            text_type_text,
        )

        got = split_nodes_image([node])

        want = [TextNode("This is text", text_type_text)]
        self.assertEqual(got, want)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        got = text_to_text_nodes(text)

        want = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(got, want)
