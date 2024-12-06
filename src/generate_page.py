import re
import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    title = re.match(r"(^#{1}\s)(.*)$", markdown, re.M)
    if title != None:
        return title.group(2)
    raise ValueError(f"Missing h1 header: {markdown}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    if os.path.exists(from_path):
        with open(from_path, "r", encoding="utf-8") as md_file:
            md_file_content = md_file.read()
    else:
        raise ValueError(f"missing or incorrect markdown path: {from_path}")
    
    # Read  template file
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as template_file:
            template = template_file.read()
    else:
        raise ValueError(f"missing or incorrect template path: {template_path}")

    html_node = markdown_to_html_node(md_file_content)
    html_string = html_node.to_html()
    title = extract_title(md_file_content)

    new_html_string = replace_tamplate_content(template, title, html_string)
    # new_html_page = 
    

def replace_tamplate_content(template, title, content):
    replaced_content = template.replace("{{ Content }}", content).replace("{{ Title }}", title)
    return replaced_content
