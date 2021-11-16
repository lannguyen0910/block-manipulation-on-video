import os
import cv2
import numpy as np
import sys
sys.path.append(".")
import utils, ffmpeg

from config import *


if __name__ == "__main__":
    
    # ------------------------- Load Blocks -------------------------
    pixel_paths = os.listdir(pixel_imgs_dir)
    pixel_paths.sort()

    if inverse:
        pixel_paths.reverse()
    
    pixels = []
    for path in pixel_paths:
        pixel = cv2.imread(os.path.join(pixel_imgs_dir,path))
        if pixel_imgs_resize != 0:
            pixel = cv2.resize(pixel,(pixel_imgs_resize,pixel_imgs_resize))
        pixels.append(pixel)
        
    pixel_size = pixels[0].shape[0]

    if len(pixels) > 2:
        level = 255 // len(pixels)
    else:
        level = 32
        
    print('Pixel shape: ', pixels[0].shape)

    # Get video infos
    print('!----------------------------------- Video infos --------------------------------------!')
    fps, endtime, height, width = ffmpeg.get_video_infos(video_path)
    scale = height / width

    utils.clean_tempfiles(False)
    utils.makedirs('./tmp/vid2img')
    utils.makedirs('./tmp/output_img')

    # Convert video into images
    print('!------------------------------ Convert video into blocks -----------------------------!')
    ffmpeg.video2image(video_path, './tmp/vid2img/%05d.png')

    # Extract audio from video
    print('!------------------------------ Extract audio from video ------------------------------!')
    ffmpeg.video2voice(video_path, './tmp/tmp.mp3')

    # Convert video frame into images of blocks
    print('!---------------------- Convert video frame into images of blocks ---------------------!')
    img_names = os.listdir('./tmp/vid2img')
    img_names.sort()

    for img_name in img_names:
        img = cv2.imread(os.path.join('./tmp/vid2img', img_name))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (output_pixel_num, int(output_pixel_num * scale)))
        
        h, w = img.shape
        out_img = np.zeros((h * pixel_size, w * pixel_size, 3), dtype = np.uint8)

        for i in range(h):
            for j in range(w):
                index = np.clip(img[i, j] // level, 0, len(pixels) - 1)
                out_img[i * pixel_size:(i + 1) * pixel_size, j * pixel_size:(j + 1) * pixel_size] = pixels[index]
        
        out_img = out_img[:(h * pixel_size // 2) * 2,:(w * pixel_size // 2) * 2]
        cv2.imwrite(os.path.join('./tmp/output_img', img_name), out_img)

    # Convert images of blocks into video of blocks
    print('!-------------------- Convert images of blocks into video of blocks -------------------!')
    ffmpeg.image2video(fps, './tmp/output_img/%05d.png', './tmp/tmp.mp3', './result.mp4')
    print('Completed!!!')