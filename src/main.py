from textnode import *
import os
import shutil
import re

def extract_title(markdown):
    title = re.match(r"(^#{1}\s)(.*)$", markdown, re.M)
    if title != None:
        return title.group(2)
    raise ValueError(f"Missing h1 header: {markdown}")

def main():

    def copy_content(current_dir=None):

        if current_dir == None:
            if os.listdir(path="public") != []:
                shutil.rmtree("public")
                os.mkdir("public")
        
        tree = []

        current_dir = "static" if current_dir == None else current_dir
        dir_content = os.listdir(path=current_dir)

        destination_path = os.path.join("public", strip_static_path(current_dir))

        for i in dir_content:
            path = os.path.join(current_dir, i)
            if os.path.isfile(path):
                shutil.copy(path, destination_path)
                tree.append(i)
            elif os.path.isdir(path):
                destination_folder = os.path.join(destination_path, i)
                os.mkdir(destination_folder)
                tree.extend([copy_content(current_dir=path)])

        return tree

    def strip_static_path(path):
        if path.startswith("static"):
            return "/".join(path.split("/")[1:])
        return path

    def generate_page(from_path, template_path, dest_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        if os.path.exists(from_path):
            with open(from_path, "r", encoding="utf-8") as md_file:
                md_file_content = md_file.read()
        else:
            raise ValueError(f"missing or incorrect path: {from_path}")


    print(copy_content())

if __name__ == "__main__":
    main()