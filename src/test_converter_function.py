import unittest

from textnode import TextNode, TextType
from converter_functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestConverterFunc(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        bold = TextNode("This is a textnode **with some bold text** within it", TextType.TEXT)
        italic = TextNode("This is a textnode *with some italic text* within it", TextType.TEXT)
        code = TextNode("This is a textnode `containing a block of code` within it", TextType.TEXT)
        
        new_bold = split_nodes_delimiter([bold], "**", TextType.BOLD)
        new_italic = split_nodes_delimiter([italic], "*", TextType.ITALIC)
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
        bold = TextNode("This is a **bold word** and this is **another bold** word", TextType.TEXT)
        italic = TextNode("This is an *italic word* and this is *another italic* word", TextType.TEXT)
        code = TextNode("This is a `code block` and here is another `code block` after it", TextType.TEXT)

        bold_italic = TextNode("This is a **bold word** and this is *an italic* word", TextType.TEXT)
        italic_code = TextNode("This is an *italic word* and this is a `code block` after it", TextType.TEXT)
        code_bold = TextNode("This is a `code block` and this is a **bold word** after it", TextType.TEXT)
        bold_italic_code = TextNode("This is a **bold word**. This is an *italic word*. And this is a `code block`.", TextType.TEXT)
        
        new_bold = split_nodes_delimiter([bold], "**", TextType.BOLD)
        new_italic = split_nodes_delimiter([italic], "*", TextType.ITALIC)
        new_code = split_nodes_delimiter([code], "`", TextType.CODE)

        new_bold_italic = split_nodes_delimiter([bold_italic], "**", TextType.BOLD)
        new_bold_italic = split_nodes_delimiter(new_bold_italic, "*", TextType.ITALIC)

        new_italic_code = split_nodes_delimiter([italic_code], "*", TextType.ITALIC)
        new_italic_code = split_nodes_delimiter(new_italic_code, "`", TextType.CODE)

        new_code_bold = split_nodes_delimiter([code_bold], "`", TextType.CODE)
        new_code_bold = split_nodes_delimiter(new_code_bold, "**", TextType.BOLD)

        new_bold_italic_code = split_nodes_delimiter([bold_italic_code], "**", TextType.BOLD)
        new_bold_italic_code = split_nodes_delimiter(new_bold_italic_code, "*", TextType.ITALIC)
        new_bold_italic_code = split_nodes_delimiter(new_bold_italic_code, "`", TextType.CODE)

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("another bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ], new_bold
        )
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("another italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)
            ], new_italic
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" after it", TextType.TEXT) 
            ], new_code
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" and this is ", TextType.TEXT),
                TextNode("an italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT) 
            ], new_bold_italic
        )
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" after it", TextType.TEXT) 
            ], new_italic_code
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(" after it", TextType.TEXT) 
            ], new_code_bold
        )
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode(". This is an ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
                TextNode(". And this is a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(".", TextType.TEXT) 
            ], new_bold_italic_code
        )

    def test_image_extractor(self):
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "Here is another ![test image](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg)"
        no_link = "Here is a failed ![image without link]() and then ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        no_alt = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        text1_test = extract_markdown_images(text1)
        text2_test = extract_markdown_images(text2)
        no_alt_test = extract_markdown_images(no_alt)

        self.assertEqual(text1_test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(text2_test, [("test image", "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg")])
        self.assertEqual(no_alt_test, [("", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

        with self.assertRaises(ValueError):
            extract_markdown_images(no_link)

    def test_link_extractor(self):
        text1 = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "Here is another [test link](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg)"
        no_link = "Here is a failed [image without link]() and then [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        no_alt = "This is text with a [](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        text1_test = extract_markdown_links(text1)
        text2_test = extract_markdown_links(text2)
        no_alt_test = extract_markdown_links(no_alt)
        image_test = extract_markdown_links(image)

        self.assertEqual(text1_test, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(text2_test, [("test link", "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg")])
        self.assertEqual(no_alt_test, [("", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(image_test, [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

        with self.assertRaises(ValueError):
            extract_markdown_links(no_link)

    def test_split_nodes_image(self):
        text1 = TextNode("Here is another ![test image](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        text2 = TextNode("![image here](https://www.imagecool.com/xtryfy/testi.img) this is a test ![number two here](https://www.imagecool.com/xtryfy/ffffffsti.img)", TextType.TEXT)
        text3 = TextNode("Here is another ![test image](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        no_url = TextNode("Here is another ![test image]() and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        no_alt = TextNode("No image text here ![](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)

        text1_test = split_nodes_image([text1])
        text2_test = split_nodes_image([text2])
        text3_test = split_nodes_image([text3])
        no_alt_test = split_nodes_image([no_alt])

        self.assertEqual([TextNode("Here is another ", TextType.TEXT),
                                      TextNode("test image", TextType.IMAGE, "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg"),
                                      TextNode(" and ", TextType.TEXT),
                                      TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")],
                                      text1_test)
        self.assertEqual([TextNode("image here", TextType.IMAGE, "https://www.imagecool.com/xtryfy/testi.img"),
                          TextNode(" this is a test ", TextType.TEXT),
                          TextNode("number two here", TextType.IMAGE, "https://www.imagecool.com/xtryfy/ffffffsti.img")],
                          text2_test)
        self.assertEqual([TextNode("Here is another ", TextType.TEXT), 
                          TextNode("test image", TextType.IMAGE, "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg"),
                          TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")],
                          text3_test)
        self.assertEqual([TextNode("No image text here ", TextType.TEXT), 
                          TextNode("", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")],
                          no_alt_test)
        
        with self.assertRaises(ValueError):
            split_nodes_image([no_url])

    def test_split_nodes_link(self):
        text1 = TextNode("Here is another [test image](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        text2 = TextNode("[image here](https://www.imagecool.com/xtryfy/testi.img) this is a test [number two here](https://www.imagecool.com/xtryfy/ffffffsti.img)", TextType.TEXT)
        text3 = TextNode("Here is another [test image](https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg)[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        no_url = TextNode("Here is another [test image]() and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        no_alt = TextNode("No image text here [](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)

        text1_test = split_nodes_link([text1])
        text2_test = split_nodes_link([text2])
        text3_test = split_nodes_link([text3])
        no_alt_test = split_nodes_link([no_alt])

        self.assertEqual([TextNode("Here is another ", TextType.TEXT),
                                      TextNode("test image", TextType.LINK, "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg"),
                                      TextNode(" and ", TextType.TEXT),
                                      TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")],
                                      text1_test)
        self.assertEqual([TextNode("image here", TextType.LINK, "https://www.imagecool.com/xtryfy/testi.img"),
                          TextNode(" this is a test ", TextType.TEXT),
                          TextNode("number two here", TextType.LINK, "https://www.imagecool.com/xtryfy/ffffffsti.img")],
                          text2_test)
        self.assertEqual([TextNode("Here is another ", TextType.TEXT), 
                          TextNode("test image", TextType.LINK, "https://www.pixelstalk.net/wp-content/uploads/2016/06/South-Park-Wallpapers-HD-Pictures.jpg"),
                          TextNode("obi wan", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")],
                          text3_test)
        self.assertEqual([TextNode("No image text here ", TextType.TEXT), 
                          TextNode("", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg")],
                          no_alt_test)
        
        with self.assertRaises(ValueError):
            split_nodes_link([no_url])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        dual_format = "This is a **bold text with a *italic text* within it**, cool huh?"

        text_test = text_to_textnodes(text)
        test_dual_format = text_to_textnodes(dual_format)

        self.assertEqual(text_test, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ])
        self.assertEqual([
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("bold text with a *italic text* within it", TextType.BOLD, None), 
            TextNode(", cool huh?", TextType.TEXT, None)],
            test_dual_format)

                          
