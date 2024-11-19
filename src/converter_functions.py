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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text.isspace() or old_node.text == "":
            continue
        if old_node.find("![") == -1:
            raise ValueError(f"missing image markdown: {old_node}")
        extracted_images = extract_markdown_images(old_node.text)
        new_nodes.extend(recursive_image(old_node.text, extracted_images))
            
    return new_nodes
    
def recursive_image(text, extracted_images, split_node=[]):
    
    if len(extracted_images) < 1:
        if len(text) < 1 or text.isspace():
            return split_node
        split_node.extend([TextNode(text, TextType.TEXT)])
        return split_node
    
    images = extracted_images.pop(0)
    text_slice = text.split(f"![{images[0]}]({images[1]})")
    
    if text.startswith("!["):
        split_node.extend([TextNode(images[0], TextType.IMAGE, images[1])])
    else:
        split_node.extend([TextNode(text_slice[0], TextType.TEXT), TextNode(images[0], TextType.IMAGE, images[1])])

    return recursive_image(text_slice[1], extracted_images, split_node)
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text.isspace() or old_node.text == "":
            continue
        if old_node.find("[") == -1:
            raise ValueError(f"missing link markdown: {old_node}")
        extracted_links = extract_markdown_links(old_node.text)
        new_nodes.extend(recursive_link(old_node.text, extracted_images))
    return new_nodes
    
def recursive_link(text, extracted_links, split_node=[]):
    
    if len(extracted_links) < 1:
        if len(text) < 1 or text.isspace():
            return split_node
        split_node.extend([TextNode(text, TextType.TEXT)])
        return split_node
    
    links = extracted_links.pop(0)
    text_slice = text.split(f"![{links[0]}]({links[1]})")
    
    if text.startswith("!["):
        split_node.extend([TextNode(links[0], TextType.LINK, links[1])])
    else:
        split_node.extend([TextNode(text_slice[0], TextType.TEXT), TextNode(links[0], TextType.LINK, links[1])])

    return recursive_image(text_slice[1], extracted_links, split_node)