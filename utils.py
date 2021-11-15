import os
import shutil


def traversal(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_list.append(os.path.join(root, file))
        for dir in dirs:
            traversal(dir)
    
    return file_list