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
        block1 = """```
this is a code block with code in it
```"""
        missing_end = """```
This is a code block with code in it
"""

        block1_test = block_to_block_type(block1)

        self.assertEqual(block1_test, "code")

        with self.assertRaises(ValueError):
            block_to_block_type(missing_end)



if __name__ == "__main__":
    unittest.main