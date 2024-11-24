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

        code_block1_test = block_to_block_type(code_block1)
        heading1_block_test = block_to_block_type(heading1_block)
        heading3_block_test = block_to_block_type(heading3_block)
        heading6_block_test = block_to_block_type(heading6_block)

        self.assertEqual(code_block1_test, "code")
        self.assertEqual(heading1_block_test, "heading")
        self.assertEqual(heading3_block_test, "heading")
        self.assertEqual(heading6_block_test, "heading")

        with self.assertRaises(ValueError):
            block_to_block_type(code_missing_end)



if __name__ == "__main__":
    unittest.main