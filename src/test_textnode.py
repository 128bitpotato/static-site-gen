import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.github.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.github.com")
        self.assertEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This i a text node", TextType.BOLD, "https://www.github.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.github.com")
        self.assertNotEqual(node, node2)
    
    def test_text_node_to_html_node(self):
        text = TextNode("This is plain text", TextType.TEXT)
        bold = TextNode("This is bold text", TextType.BOLD)
        italic = TextNode("This is italic text", TextType.ITALIC)
        code = TextNode("This is a slice of code", TextType.CODE)
        link = TextNode("This is a link", TextType.LINK, "https://www.github.com")
        image = TextNode("This is an image", TextType.IMAGE, "https://www.github.com")
        exception = TextNode("This is a slice of code", "bold")

        text_html = text_node_to_html_node(text)
        bold_html = text_node_to_html_node(bold)
        italic_html = text_node_to_html_node(italic)
        code_html = text_node_to_html_node(code)
        link_html = text_node_to_html_node(link)
        image_html = text_node_to_html_node(image)

        self.assertEqual(text_html.__repr__(), 'LeafNode(None, This is plain text, None)')
        self.assertEqual(bold_html.tag, "b")
        self.assertEqual(italic_html.value, "This is italic text")
        self.assertEqual(code_html.tag, "code")
        self.assertEqual(link_html.to_html(), '<a href="https://www.github.com">This is a link</a>')
        self.assertEqual(image_html.props, {"src": "https://www.github.com", "alt": "This is an image"})

        with self.assertRaises(Exception):
            text_node_to_html_node(exception)

if __name__ == "__main__":
    unittest.main()