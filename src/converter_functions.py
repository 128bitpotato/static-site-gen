from textnode import *

delimiters = {"**": TextType.BOLD,
              "*": TextType.ITALIC}

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    for node in old_nodes:
        split_list = node.text.split(delimiter)

        starting_type = text_type if node.text.startswith(delimiter) else node.text_type
        type_dict = {"start": starting_type, "other": text_type if starting_type != text_type else node.text_type}
           
        new_nodes = list(map(
            lambda num, string: TextNode(string, 
                                type_dict["start"] if (num % 2 == 0) else type_dict["other"]), 
                                range(len(split_list)), split_list)) # Range-number of split list to decide node_type

        list_of_nodes.extend(new_nodes)

    return list_of_nodes
        