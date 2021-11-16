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

def is_video(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.mp4','.flv','.avi','.mov','.mkv','.wmv','.rmvb','.mts']:
        return True

    return False

def is_videos(paths):
    tmp = []
    for path in paths:
        if is_video(path):
            tmp.append(path)
    return tmp 

def writelog(path,log):
    f = open(path, 'a+')
    f.write(log + '\n')
    f.close()

def makedirs(path):
    if os.path.isdir(path):
        print(path,' existed')
    else:
        os.makedirs(path)
        print('Makedir: ', path)

def copyfile(src, dst):
    try:
        shutil.copyfile(src, dst)
    except Exception as e:
        print(e)

def clean_tempfiles(tmp_init=True):
    if os.path.isdir('./tmp'):   
        shutil.rmtree('./tmp')
    if tmp_init:
        os.makedirs('./tmp')
        os.makedirs('./tmp/video_voice')    
        os.makedirs('./tmp/music/')
        os.makedirs('./tmp/video_img')
        os.makedirs('./tmp/vid2img')
        os.makedirs('./tmp/output_img')