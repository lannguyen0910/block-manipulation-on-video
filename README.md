# <p align="center"> Manipulate blocks on video </p>


https://user-images.githubusercontent.com/47696901/141905787-2bb79845-4493-436d-a8ef-63137ab5d8b3.mp4

<p align="center">
  <a style="font-size: 40px; color:red;"> <strong> Turn on sound to listen to the music (Bad Apple) </strong> </a>
</p>

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


## **Get subprocess stdout**
```python

def run(args, mode = 0):
    if mode == 0:
        cmd = args2cmd(args)
        os.system(cmd)

    elif mode == 1:
        cmd = args2cmd(args)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout = p.communicate()[0]
        print('Stdout: ', sout)
        
        return sout

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
