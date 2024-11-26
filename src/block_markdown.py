import re

html_tags = {"quote": "blockquote",
             "unordered_list": "ul",
             "ordered_list": "ol",
             "code": "code",
             "heading": "h",
             "paragraph": "p"}

def markdown_to_html_node(markdown):
    list_of_blocks = markdown_to_blocks(markdown)
    for block in list_of_blocks:
        block_type = block_to_block_type(block)

def block_to_html_tag(block):
    tag = html_tags[block_to_block_type(block)]
    if tag == "code":
        tag = "pre"
    if tag == "h":
        match = re.match(r"(^#{1,6})", block)
        tag += str(len(match.group(1)))
    return tag


def text_to_children(text):
    pass

def markdown_to_blocks(markdown):
    remove_space = "\n".join(list(
        map(lambda line: line.strip() if line.isspace() else line, 
            markdown.splitlines()
            )))

    split_blocks = list(
        filter(lambda block: block != "", list( # filter empty blocks
            map(lambda block: block.strip(),    # strip leading and trailing whitespaces
                remove_space.split("\n\n")      # split text at blank line
                ))))
    return split_blocks

def block_to_block_type(block):

    # Error handling
    if block == "" or block.isspace():
        raise ValueError(f"Empty block: ({block})")

    # Headings
    if re.match(r"(^#{1,6}\s)", block):
        return "heading"

    #Code block
    if block.startswith("```"):
        if not block.endswith("```"):
            raise ValueError(f'unclosed code block. code blocks needs to end with "```": {block}')
        return "code"
    
    # Quote block
    if block.startswith(">"):
        if re.match(r"^(> .*)?$|^(>)$", block, re.M):
            return "quote"
        else:
            raise ValueError(f"Missing > in block quote, all lines need to start with >: {block}")

    # Unordered list
    if block.startswith("* ") or block.startswith("- "):
        if re.match(r"^(\* .*|\- .*)?$", block, re.M):
            return "unordered_list"
        else:
            raise ValueError(f"Invalid list syntax, every line must start with * or - followed by a space: {block}")


    # Ordered list
    if re.match(r"^(\d\.\s.*)?$", block.splitlines()[0]):
        for num, line in enumerate(block.splitlines(), start=1):
            if not re.match(rf"^({num}\.\s.*)?$", line):
                raise ValueError(f'Invalid ordered list syntax: {block}')
            return "ordered_list"
    
    # Paragraph
    return "paragraph"