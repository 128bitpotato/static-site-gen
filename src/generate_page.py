import re
import os
import shutil

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

    # Convert markdown to html
    html_node = markdown_to_html_node(md_file_content)
    content = html_node.to_html()
    title = extract_title(md_file_content)
    new_html_string = template.replace("{{ Content }}", content).replace("{{ Title }}", title)


    # Create new html file
    dest_file_name = destination_file_name(dest_path)

    with open(dest_file_name, "w") as new_html_page:
        new_html_page.write(new_html_string)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Check every item in content folder
    for i in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, i)

        # If item is file, generate html page
        if os.path.isfile(path):
            destination_file = os.path.join(dest_dir_path, i)
            generate_page(path, template_path, destination_file)

        # If item is folder, recursive call for folder
        elif os.path.isdir(path):
            destination_folder = os.path.join(dest_dir_path, i)
            if not os.path.isdir(destination_folder):
                os.mkdir(destination_folder)
            
            generate_pages_recursive(path, template_path, destination_folder)
            

def replace_tamplate_content(template, title, content):
    replaced_content = template.replace("{{ Content }}", content).replace("{{ Title }}", title)
    return replaced_content

def strip_static_path(path):
    if path.startswith("static"):
        return "/".join(path.split("/")[1:])
    return path

def destination_file_name(dest_path):
    dest_file_name = os.path.basename(dest_path)
    split_name = dest_file_name.split(".")
    html_file = split_name[0] + ".html"
    dir_name = os.path.dirname(dest_path)
    new_path = os.path.join(dir_name, html_file)
    return new_path
