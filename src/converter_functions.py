import re
from textnode import *

delimiters = {"**": TextType.BOLD,
              "*": TextType.ITALIC}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_nodes.append(node)
            continue
        if node.text.find(delimiter) == -1:
            list_of_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("delimiter not closed, invalid number of sections")

        starting_type = text_type if node.text.startswith(delimiter) else node.text_type
        type_dict = {"start": starting_type, "other": text_type if starting_type != text_type else node.text_type}
           
        new_nodes = list(map(
            lambda num, string: TextNode(string, 
                                type_dict["start"] if (num % 2 == 0) else type_dict["other"]), 
                                range(len(sections)), sections)) # Range-number of split list to decide node_type

        list_of_nodes.extend(new_nodes)

    return list_of_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.finditer(pattern=pattern, string=text)
    extracted_images = []

    for match in matches:
        alt = match.group(1)
        url = match.group(2)
        if url == "":
            raise ValueError("url missing. Image must have url to function")
        extracted_images.append((alt, url))

    return extracted_images

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.finditer(pattern=pattern, string=text)
    extracted_images = []

    for match in matches:
        alt = match.group(1)
        url = match.group(2)
        if url == "":
            raise ValueError("url missing. Image must have url to function")
        extracted_images.append((alt, url))

    return extracted_images