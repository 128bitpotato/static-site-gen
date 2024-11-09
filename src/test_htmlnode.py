import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_props_func1(self):
        node = HTMLNode("p", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro"})
        propos = node.props_to_html()
        self.assertTrue(propos == ' class="main_text" id="intro"')

    def test_no_props_func(self):
        node = HTMLNode("b", "This is a string, cool huh?")
        propos = node.props_to_html()
        self.assertFalse(propos == ' class="main_text" id="intro" test="nummer"')

    def test_values(self):
        node = HTMLNode("b", "This is a string, cool huh?")
        node2 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})

        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "This is a string, cool huh?")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node2.props, {"href": "https://www.google.com", "target": "_blank"})
        
    def test_repr(self):
        node = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, This is a link, children: None, {'href': 'https://www.google.com', 'target': '_blank'})")

    def test_many_nodes(self):
        node1 = HTMLNode("p", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro"})
        node2 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        node3 = HTMLNode("b", "Big fat bold text", None, {"color": "brown"})
        node4 = HTMLNode("h1", "Heading")
        node5 = HTMLNode("p", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro"})
        pass

    def test_raise(self):
        node1 = HTMLNode("p", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro"})
        with self.assertRaises(NotImplementedError):
            node1.to_html()
    
    def test_leaf(self):
        child = LeafNode(tag="a", value="This is a link", props={"href": "https://www.google.com"})
        child2 = LeafNode(None, "This is raw text", None)
        child3 = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(child.tag, "a")
        self.assertEqual(child.value, "This is a link")
        self.assertEqual(child.props, {"href": "https://www.google.com"})
        self.assertEqual(child.to_html(), '<a href="https://www.google.com">This is a link</a>')
        self.assertEqual(child2.to_html(), "This is raw text")
        self.assertEqual(child3.to_html(), "<p>This is a paragraph of text</p>")

    def test_leaf_raise(self):
        child = LeafNode(tag="a", value=None, props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            child.to_html()

    def test_parent_node(self):
        parent = ParentNode(tag="p", children=[LeafNode("b", "Bold text"),
                                  LeafNode(None, "Normal text"),
                                  LeafNode("i", "italic text"),
                                  LeafNode(None, "Normal text")])
        self.assertEqual(parent.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")


if __name__ == "__main__":
    unittest.main