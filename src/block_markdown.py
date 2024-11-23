
def markdown_to_blocks(markdown):
    split_blocks = list(
        filter(lambda block: block != "", list( # filter empty blocks
            map(lambda block: block.strip(),    # strip leading and trailing whitespaces
                markdown.split("\n\n")          # split text at blank line
                ))))
    return split_blocks
