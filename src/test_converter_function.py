import unittest

from textnode import TextNode, TextType
from converter_functions import split_nodes_delimiter


class TestConverterFunc(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        bold = TextNode("This is a textnode *with some bold text* within it", TextType.TEXT)
        italic = TextNode("This is a textnode **with some italic text** within it", TextType.TEXT)
        code = TextNode("This is a textnode `containing a block of code` within it", TextType.TEXT)
        
        new_bold = split_nodes_delimiter([bold], "*", TextType.BOLD)
        new_italic = split_nodes_delimiter([italic], "**", TextType.ITALIC)
        new_code = split_nodes_delimiter([code], "`", TextType.CODE)

        self.assertListEqual(
            [
                TextNode("This is a textnode ", TextType.TEXT),
                TextNode("with some bold text", TextType.BOLD),
                TextNode(" within it", TextType.TEXT)
            ], new_bold
        )
        self.assertListEqual(
            [
                TextNode("This is a textnode ", TextType.TEXT),
                TextNode("with some italic text", TextType.ITALIC),
                TextNode(" within it", TextType.TEXT)
            ], new_italic
        )
        self.assertListEqual(
            [
                TextNode("This is a textnode ", TextType.TEXT),
                TextNode("containing a block of code", TextType.CODE),
                TextNode(" within it", TextType.TEXT)
            ], new_code
        )
    
    def test_multiple_delimiters(self):
        bold = TextNode("This is a *bold word* and this is *another bold* word", TextType.TEXT)
        italic = TextNode("This is an **italic word** and this is **another italic** word", TextType.TEXT)
        code = TextNode("This is a `code block` and here is another `code block` after it", TextType.TEXT)

        bold_italic = TextNode("This is a *bold word* and this is **an italic** word", TextType.TEXT)
        italic_code = TextNode("This is an **italic word** and this is a `code block` after it", TextType.TEXT)
        code_bold = TextNode("This is a `code block` and this is a *bold word* after it", TextType.TEXT)
        bold_italic_code = TextNode("This is a *bold word.* This is an **italic word.** And this is a `code block`.")
        
        new_bold = split_nodes_delimiter([bold], "*", TextType.BOLD)
        new_italic = split_nodes_delimiter([italic], "**", TextType.ITALIC)
        new_code = split_nodes_delimiter([code], "`", TextType.CODE)

        