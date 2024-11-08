import unittest

from htmlnode import HTMLNode, LeafNode


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
        node1 = HTMLNode("a", "This is a link", None, {"href": "https://www.google.com", "target": "_blank"})
        child = LeafNode(node1)
        self.assertEqual(child, node1.tag)
        self.assertEqual(child, node1.value)
        self.assertEqual(child, node1.props)
        self.assertEqual(child.to_html, "<a href=https://www.google.com>This is a link</a>")



if __name__ == "__main__":
    unittest.main