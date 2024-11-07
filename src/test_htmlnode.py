import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_props_func1(self):
        node = HTMLNode("p", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro"})
        propos = node.props_to_html()
        self.assertTrue(propos == ' class="main_text" id="intro"')

    def test_props_func2(self):
        node = HTMLNode("b", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro", "test": "nummer"})
        propos = node.props_to_html()
        self.assertTrue(propos == ' class="main_text" id="intro" test="nummer"')

    def test_props_func3(self):
        node = HTMLNode("b", "This is a string, cool huh?", None, {"class": "main_text", "id": "intro", "test": "nummer", "test2": "kronan"})
        propos = node.props_to_html()
        self.assertFalse(propos == ' class="main_text" id="intro" test="nummer"')

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

if __name__ == "__main__":
    unittest.main