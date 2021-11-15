import os, json
import subprocess

def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd

def run(args,mode = 0):

    if mode == 0:
        cmd = args2cmd(args)
        os.system(cmd)

    elif mode == 1:
        cmd = args2cmd(args)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout = p.stdout.readlines()
        return sout

def get_video_infos(videopath):
    args =  ['ffprobe -v quiet -print_format json -show_format -show_streams', '-i', '"'+videopath+'"']

    out_string = run(args,mode=0)

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

    return fps,endtime,height,width