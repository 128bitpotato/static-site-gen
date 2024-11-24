import re

def markdown_to_blocks(markdown):
    remove_space = "\n".join(list(
        map(lambda line: line.strip() if line.isspace() else line, 
            markdown.split("\n")
            )))

    split_blocks = list(
        filter(lambda block: block != "", list( # filter empty blocks
            map(lambda block: block.strip(),    # strip leading and trailing whitespaces
                remove_space.split("\n\n")      # split text at blank line
                ))))
    return split_blocks

def block_to_block_type(block):
    # Headings
    if re.match(r"(^#{1,6}\s)", block):
        return "heading"

    #Code block
    if block.startswith("```"):
        if not block.endswith("```"):
            raise ValueError(f'code blocks needs to end with "```": {block}')
        return "code"
    
    # Quote block


    # Unordered list


    # Ordered list
        