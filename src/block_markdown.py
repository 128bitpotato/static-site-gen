
def markdown_to_blocks(markdown):
    remove_space = "\n".join(list(
        map(lambda line: line.strip() if line.isspace() else line, 
            markdown.split("\n")
            )))

    split_blocks = list(
        filter(lambda block: block != "", list( # filter empty blocks
            map(lambda block: block.strip(),    # strip leading and trailing whitespaces
                remove_space.split("\n\n")          # split text at blank line
                ))))
    return split_blocks
