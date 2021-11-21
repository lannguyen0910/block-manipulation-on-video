# <p align="center"> Convert video into blocks </p>


https://user-images.githubusercontent.com/47696901/141905787-2bb79845-4493-436d-a8ef-63137ab5d8b3.mp4

<p align="center">
  <a style="font-size: 40px; color:red;"> <strong> Turn on sound to listen to the music (Bad Apple, play on web browser only!) </strong> </a>
</p>

![gif](./demo/result.gif)

# **Setup and run (Linux)**
- Python3 and [ffmpeg](http://ffmpeg.org/).
```
sudo apt-get install ffmpeg
```
- Install other dependencies.
```
pip install requirements.txt
```

- Download your own video and change values in config file to your own interests. 

- Use shell script to clear ```__pycache__``` cache after running.
```
run.bat
```

- **Notice: The result video cannot play on mobile devices yet. Update in the future!**


## **Convert images from video to images of blocks**
```python

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
```

## **Get video infos**
```python

def get_video_infos(videopath):
    args =  ['ffprobe -v quiet -print_format json -show_format -show_streams', '-i', '"' + videopath + '"']

    out_string = run(args, mode=1)

    infos = json.loads(out_string)
    try:
        fps = eval(infos['streams'][0]['avg_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][0]['width'])
        height = int(infos['streams'][0]['height'])

    except Exception as e:
        fps = eval(infos['streams'][1]['r_frame_rate'])
        endtime = float(infos['format']['duration'])
        width = int(infos['streams'][1]['width'])
        height = int(infos['streams'][1]['height'])

    return fps, endtime, height, width
```

## **Convert video to ịmages**
```python

def video2image(videopath, imagepath, fps=0, start_time='00:00:00', last_time='00:00:00'):
    args = ['ffmpeg', '-i', '"'+videopath+'"']
    if last_time != '00:00:00':
        args += ['-ss', start_time]
        args += ['-t', last_time]
    if fps != 0:
        args += ['-r', str(fps)]
    args += ['-f', 'image2','-q:v','-0',imagepath]

    run(args)

```

## **Convert images to video**
```python

def image2video(fps, imagepath, voicepath, videopath):
    if voicepath != None:
        os.system('ffmpeg -y -r ' + str(fps) + ' -i ' + imagepath + ' -vcodec libx264 ' + './tmp/video_tmp.mp4')
        os.system('ffmpeg -i ./tmp/video_tmp.mp4 -i "'+voicepath+'" -vcodec copy -acodec aac ' + videopath)
    else:
        os.system('ffmpeg -y -r ' + str(fps) + ' -i '+ imagepath + ' -vcodec libx264 ' + videopath)

```

## **Extract audio from video**
```python

def video2voice(videopath, voicepath, start_time='00:00:00', last_time='00:00:00'):
    args = ['ffmpeg', '-i', '"' + videopath + '"','-f mp3','-b:a 320k']
    if last_time != '00:00:00':
        args += ['-ss', start_time]
        args += ['-t', last_time]
    args += [voicepath]
    
    run(args)

```
