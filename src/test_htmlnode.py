from htmlnode import HTMLNode, LeafNode, ParentNode
import unittest


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a", "a link!", None, {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.propsToHTML(), 'href="https://www.google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            value="a link!",
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.toHTML(),
            '<a href="https://www.google.com" target="_blank">a link!</a>',
        )

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
            tag="p",
        )
        self.assertEqual(node.toHTML(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parent_to_html(self):
        child1 = ParentNode(
            children=[
                LeafNode(tag="b", value="Bold text", props={"abc": 123}),
                LeafNode(tag=None, value="Normal text"),
            ],
            tag="p"
        )
        node = ParentNode(
            children=[
                child1,
                LeafNode(tag="i", value="Italic text")
            ],
            tag="p"
        )
        self.assertEqual(node.toHTML(), '<p><p><b abc="123">Bold text</b>Normal text</p><i>Italic text</i></p>')


    def test_double_nested_parent_to_html(self):
        child1 = ParentNode(
            children=[
                LeafNode(tag="b", value="Bold text", props={"abc": 123}),
                LeafNode(tag=None, value="Normal text"),
            ],
            tag="p"
        )
        child2 = ParentNode(
            children=[
                LeafNode(tag="div", value="Bold text", props={"": 123}),
                LeafNode(tag=None, value="Normal text"),
            ],
            tag="div"
        )
        child3 = ParentNode(
            children=[
                child2,
                LeafNode(tag=None, value="Normal text"),
            ],
            tag="span"
        )
        node = ParentNode(
            children=[
                child1,
                child3,
                LeafNode(tag="i", value="Italic text")
            ],
            tag="p"
        )
        self.assertEqual(node.toHTML(), '<p><p><b abc="123">Bold text</b>Normal text</p><span><div><div ="123">Bold text</div>Normal text</div>Normal text</span><i>Italic text</i></p>')
        
