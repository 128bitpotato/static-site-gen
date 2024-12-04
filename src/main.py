from textnode import *
import os
import shutil

def main():

    def copy_content(tree=None, current_dir=None):

        # if os.listdir(path="public") != []:
        #     if tree == None:
        #         shutil.rmtree("public")
        #         os.mkdir("public")
        
        if tree is None:
            tree = []

        current_dir = "static" if current_dir == None else current_dir
        dir_content = os.listdir(path=current_dir)
        for i in dir_content:
            path = os.path.join(current_dir, i)
            if os.path.isfile(path):
                tree.append(i)
            elif os.path.isdir(path):
                tree.extend([copy_content(tree=None, current_dir=path)])

        return tree



            


        # os.path.exists("static/")
        # dir = os.listdir(path="static/")
        return False
    
    print(copy_content())

if __name__ == "__main__":
    main()