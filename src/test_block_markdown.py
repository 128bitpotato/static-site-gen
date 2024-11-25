import unittest

from block_markdown import markdown_to_blocks, block_to_block_type

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



if __name__ == "__main__":
    unittest.main