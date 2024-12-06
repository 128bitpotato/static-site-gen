from textnode import *
import os
import shutil
import re

from copy_path import copy_content
from generate_page import generate_pages_recursive

def main():

    if os.listdir(path="public") != []:
        shutil.rmtree("public")
        os.mkdir("public")
    
    if os.listdir(path="static") == []:
        raise ValueError("Missing content in static folder")
    copy_content()

    content_path = os.path.join("content")
    template_path = os.path.join("template.html")
    dest_path = os.path.join("public")
    generate_pages_recursive(content_path, template_path, dest_path)



    

if __name__ == "__main__":
    main()