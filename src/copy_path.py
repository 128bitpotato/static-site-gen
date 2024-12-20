import os
import shutil

def copy_content(current_dir=None):
        
    tree = [] # Only for debugging

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