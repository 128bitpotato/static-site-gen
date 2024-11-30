import unittest

from htmlnode import *

from block_markdown import markdown_to_blocks, block_to_block_type, remove_markdown_syntax, text_to_children, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text1 = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        text1_test = markdown_to_blocks(text1)

        self.assertEqual(['# This is a heading', 
                          'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                          '* This is the first list item in a list block\n* This is a list item\n* This is another list item'],
                          text1_test)
        
        empty_spaces = """# This is a heading
      
This is a paragraph of text. It has some **bold** and *italic* words inside of it.     

* This is the first list item in a list block
* This is a list item
* This is another list item      """

        test_empty_spaces = markdown_to_blocks(empty_spaces)

        self.assertEqual(['# This is a heading', 
                          'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                          '* This is the first list item in a list block\n* This is a list item\n* This is another list item'],
                          test_empty_spaces)
        
        
    def test_block_to_block_type(self):
        code_block1 = """```
this is a code block with code in it
```"""
        code_missing_end = """```
This is a code block with code in it
"""
        heading1_block = "# Heading 1"
        heading3_block = "### Heading 3"
        heading6_block = "###### Heading 6"

        quote_block = "> this is a quote"
        quote_block_multi = """> This is a quote
> in multiple lines
> that should work
>
> and that is all."""
        quote_block_multi_error = """> this quote
>
> shouldnt work
because its wrong
>"""
        unordered_list = """* line one
* line two
* line three
* line four"""
        unordered_list2 = """- line one
- line two
- line three
- line four"""
        unordered_list3 = """- line one
* line two
- line three
* line four"""
        unordered_list_error = """- line one
- line two
line three
- line four"""

        ordered_list1 = """1. object 1
2. object 2
3. object three
4. object 4"""
        ordered_list_error = """1. object 1
3. object 2
4. object three
4. object 4"""
        ordered_list_error2 = """3. object 1
4. object 2
5. object three
6. object 4"""

        paragraph1 = "This is a paragraph"
        paragraph2 = "This is a paragraph with **bold text** and *italic text*"
        paragraph3 = "`this paragraph starts` with a code block"
        paragraph_no_list = "-This isn't a list, its something else"
        paragraph_no_list2 = "*I dont know why I use star here. Sorry..."

        error_handling1 = ""
        error_handling2 = "          "

        code_block1_test = block_to_block_type(code_block1)
        heading1_block_test = block_to_block_type(heading1_block)
        heading3_block_test = block_to_block_type(heading3_block)
        heading6_block_test = block_to_block_type(heading6_block)

        quote_block_test = block_to_block_type(quote_block)
        quote_block_multi_test = block_to_block_type(quote_block_multi)

        unordered_list_test = block_to_block_type(unordered_list)
        unordered_list2_test = block_to_block_type(unordered_list2)
        unordered_list3_test = block_to_block_type(unordered_list3)
        ordered_list1_test = block_to_block_type(ordered_list1)

        paragraph1_test = block_to_block_type(paragraph1)
        paragraph2_test = block_to_block_type(paragraph2)
        paragraph3_test = block_to_block_type(paragraph3)
        paragraph_no_list_test = block_to_block_type(paragraph_no_list)
        paragraph_no_list2_test = block_to_block_type(paragraph_no_list2)

        self.assertEqual(code_block1_test, "code")

        self.assertEqual(heading1_block_test, "heading")
        self.assertEqual(heading3_block_test, "heading")
        self.assertEqual(heading6_block_test, "heading")

        self.assertEqual(quote_block_test, "quote")
        self.assertEqual(quote_block_multi_test, "quote")

        self.assertEqual(unordered_list_test, "unordered_list")
        self.assertEqual(unordered_list2_test, "unordered_list")
        self.assertEqual(unordered_list3_test, "unordered_list")

        self.assertEqual(ordered_list1_test, "ordered_list")

        self.assertEqual(paragraph1_test, "paragraph")
        self.assertEqual(paragraph2_test, "paragraph")
        self.assertEqual(paragraph3_test, "paragraph")
        self.assertEqual(paragraph_no_list_test, "paragraph")
        self.assertEqual(paragraph_no_list2_test, "paragraph")

        with self.assertRaises(ValueError):
            block_to_block_type(code_missing_end)
            block_to_block_type(quote_block_multi_error)
            block_to_block_type(unordered_list_error)
            block_to_block_type(ordered_list_error)
            block_to_block_type(ordered_list_error2)
            block_to_block_type(error_handling1)
            block_to_block_type(error_handling2)

    def test_remove_markdown_syntax(self):
        quote = """> This is a quote
> in multiple lines
> that should work
>
> and that is all."""
        heading = "# Heading 1"
        heading3 = "### Heading 3"
        heading6 = "###### Heading 6"
        code = """```
this is a code block with code in it
```"""
        unordered_list = """* line one
* line two
* line three
* line four"""
        ordered_list = """1. object 1
2. object 2
3. object three
4. object 4"""

        quote_test = remove_markdown_syntax(quote, "quote")
        heading_test = remove_markdown_syntax(heading, "heading")
        heading3_test = remove_markdown_syntax(heading3, "heading")
        heading6_test = remove_markdown_syntax(heading6, "heading")
        code_test = remove_markdown_syntax(code, "code")
        unordered_list_test = remove_markdown_syntax(unordered_list, "unordered_list")
        ordered_list_test = remove_markdown_syntax(ordered_list, "ordered_list")

        self.assertEqual(quote_test, """This is a quote
in multiple lines
that should work

and that is all.""")
        self.assertEqual(heading_test, "Heading 1")
        self.assertEqual(heading3_test, "Heading 3")
        self.assertEqual(heading6_test, "Heading 6")
        self.assertEqual(code_test, "`this is a code block with code in it`")
        self.assertEqual(unordered_list_test, """line one
line two
line three
line four""")
        self.assertEqual(ordered_list_test, """object 1
object 2
object three
object 4""")
    
    def test_childnode(self):
        test1 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        test1_test = text_to_children(test1)

        self.assertListEqual([LeafNode(None, "This is ", None), 
                          LeafNode("b", "text", None), 
                          LeafNode(None, " with an ", None), 
                          LeafNode("i", "italic", None), 
                          LeafNode(None, " word and a ", None), 
                          LeafNode("code", "code block", None), 
                          LeafNode(None, " and an ", None), 
                          LeafNode("img", "", {'src': 'https://i.imgur.com/fJRm4Vk.jpeg', 'alt': 'obi wan image'}), 
                          LeafNode(None, " and a ", None), LeafNode("a", "link", {'href': 'https://boot.dev'})],
                          test1_test)
        
    def test_markdown_to_html(self):
        heading = "### Heading 3"
        quote = """> This is a quote
> in multiple lines
> that should work
>
> and that is all."""
        unordered_list = """* line one
* line two
* line three
* line four"""
        ordered_list = """1. line one
2. line two
3. line three
4. line four"""
        code = """```
this is a code block with code in it
and here it is as well
and more over here
```"""
        paragraph = "This is simple text with an *italic* word and a **bold** word. Lastly there's a `code block` and a ![picture](https://www.google.com/picture.gif) and then a [link](https://www.boot.dev/profile)"
        all_syntax = heading + "\n\n" + quote + "\n\n" + unordered_list + "\n\n" + ordered_list + "\n\n" + code + "\n\n" + paragraph

        heading_test = markdown_to_html_node(heading)
        quote_test = markdown_to_html_node(quote)
        unordered_list_test = markdown_to_html_node(unordered_list)
        ordered_list_test = markdown_to_html_node(ordered_list)
        code_test = markdown_to_html_node(code)
        paragraph_test = markdown_to_html_node(paragraph)
        all_syntax_test = markdown_to_html_node(all_syntax)
        
        self.assertEqual(heading_test, ParentNode("div", 
                                                  [ParentNode("h3", 
                                                              [LeafNode(None, "Heading 3")])]),
                                                              )
        self.assertEqual(quote_test, ParentNode("div", 
                                                [ParentNode("blockquote", 
                                                            [LeafNode(None, """This is a quote
in multiple lines
that should work

and that is all.""")])])
                                                            )
        self.assertEqual(unordered_list_test, ParentNode("div", 
                                                         [ParentNode("ul", [
                                                             LeafNode("li", "line one"), 
                                                             LeafNode("li", "line two"),
                                                             LeafNode("li", "line three"),
                                                             LeafNode("li", "line four")])])
                                                             )
        self.assertEqual(ordered_list_test, ParentNode("div", 
                                                         [ParentNode("ol", [
                                                             LeafNode("li", "line one"), 
                                                             LeafNode("li", "line two"),
                                                             LeafNode("li", "line three"),
                                                             LeafNode("li", "line four")])])
                                                             )
        self.assertEqual(code_test, ParentNode("div", 
                                               [ParentNode("pre", 
                                                           [LeafNode("code", """this is a code block with code in it
and here it is as well
and more over here""")])]))
        self.assertEqual(paragraph_test, ParentNode("div", 
                                                    [ParentNode("p", [
                                                        LeafNode(None, "This is simple text with an "),
                                                        LeafNode("i", "italic"),
                                                        LeafNode(None, " word and a "),
                                                        LeafNode("b", "bold"),
                                                        LeafNode(None, " word. Lastly there's a "),
                                                        LeafNode("code", "code block"),
                                                        LeafNode(None, " and a "),
                                                        LeafNode("img", "", {"src": "https://www.google.com/picture.gif", 
                                                                               "alt": "picture"}),
                                                        LeafNode(None, " and then a "),
                                                        LeafNode("a", "link", {"href": "https://www.boot.dev/profile"})])]))
        self.assertEqual(all_syntax_test, ParentNode("div", [ParentNode("h3", 
                                                              [LeafNode(None, "Heading 3")]),
                                                              ParentNode("blockquote", 
                                                                         [LeafNode(None, """This is a quote
in multiple lines
that should work

and that is all.""")]),
                                                            ParentNode("ul", [
                                                                LeafNode("li", "line one"), 
                                                                LeafNode("li", "line two"),
                                                                LeafNode("li", "line three"),
                                                                LeafNode("li", "line four")]),
                                                            ParentNode("ol", [
                                                             LeafNode("li", "line one"), 
                                                             LeafNode("li", "line two"),
                                                             LeafNode("li", "line three"),
                                                             LeafNode("li", "line four")]),
                                                             ParentNode("pre", 
                                                           [LeafNode("code", """this is a code block with code in it
and here it is as well
and more over here""")]),
                                                            ParentNode("p", [
                                                                LeafNode(None, "This is simple text with an "),
                                                                LeafNode("i", "italic"),
                                                                LeafNode(None, " word and a "),
                                                                LeafNode("b", "bold"),
                                                                LeafNode(None, " word. Lastly there's a "),
                                                                LeafNode("code", "code block"),
                                                                LeafNode(None, " and a "),
                                                                LeafNode("img", "", {"src": "https://www.google.com/picture.gif", 
                                                                               "alt": "picture"}),
                                                                LeafNode(None, " and then a "),
                                                                LeafNode("a", "link", {"href": "https://www.boot.dev/profile"})])])
                                                                )

if __name__ == "__main__":
    unittest.main()