import re
import os

def extract_title(markdown):
    title = re.match(r"(^#{1}\s)(.*)$", markdown, re.M)
    if title != None:
        return title.group(2)
    raise ValueError(f"Missing h1 header: {markdown}")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if os.path.exists(from_path):
        with open(from_path, "r", encoding="utf-8") as md_file:
            md_file_content = md_file.read()
    else:
        raise ValueError(f"missing or incorrect path: {from_path}")