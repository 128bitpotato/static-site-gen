from textnode import *
import os
import shutil
import re

from copy_path import copy_content
from generate_page import extract_title, generate_page

def main():

    if os.listdir(path="public") != []:
        shutil.rmtree("public")
        os.mkdir("public")
    
    if os.listdir(path="static") == []:
        raise ValueError("Missing content in static folder")
    copy_content()

    from_path = os.path.join("content", "index.md")
    template_path = os.path.join("template.html")
    dest_path = os.path.join("public", "index.html")
    generate_page(from_path, template_path, dest_path)




    

if __name__ == "__main__":
    main()