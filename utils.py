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

def is_img(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        return True
    
    return False

def is_imgs(paths):
    tmp = []
    for path in paths:
        if is_img(path):
            tmp.append(path)
    
    return tmp