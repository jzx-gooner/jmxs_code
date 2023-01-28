# 工具：开启进程函数，杀掉进程函数等其他杂七杂八
# author:jzx
import shutil
import psutil
import os
import signal
import subprocess
import cv2
import time
import sys

def kill_deepstream():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'deepstream-test5-analytics':
            os.kill(pid,signal.SIGKILL)

def kill_arcface():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == 'pro':
            os.kill(pid,signal.SIGKILL)

def start_deepstream():
    a = subprocess.Popen("sh go_deepstream.sh",stdout=sys.stdout,stderr=sys.stderr,shell=True)
    print(a.poll())
    time.sleep(5)
    print(a.poll())
    return


def start_redis_server():
    a = subprocess.Popen("redis-server",stdout=sys.stdout,stderr=sys.stderr,shell=True)
    print(a.poll())
    time.sleep(5)
    print(a.poll())
    return

def draw_bounding_box(labels_txt):
    with open(labels_txt) as f:
        print(labels_txt)
        raw_img = labels_txt.replace("labels.txt","image.png")
        print(raw_img)
        image = cv2.imread(raw_img)
        temp = str(time.time()).replace(".","")
        save_jpg_name = labels_txt.replace("labels.txt",temp+".jpg").replace("images","save_result")
        lines = f.readlines()
        for line in lines:
            label = line.split(" ")[0]
            confidence = line.split(" ")[-1]
            confidence = round(float(confidence),2)
            top_left_x,top_left_y,down_right_x,down_right_y = [int(float(s)) for s in line.split(" ")[1:-1]]
            cv2.rectangle(image,(top_left_x,top_left_y),(down_right_x,down_right_y),(0,255,0),2)
            cv2.putText(image,label+" : "+str(confidence),(top_left_x,top_left_y+10),fontScale = 1,fontFace=1 ,color=(255,0,0),thickness = 2)
            print(save_jpg_name)
            cv2.imwrite(save_jpg_name,image)    

        return save_jpg_name

def build_engine():
    if not os.path.exists("/configs_dir/jmxs.engine"):
        print("解密模型")
        print("移动升级模型")            
        a = subprocess.Popen("sh go_build_engine.sh",stdout=sys.stdout,stderr=sys.stderr,shell=True)
        while(1):
            if(os.path.exists("/configs_dir/jmxs.engine")):
                time.sleep(10)
                print("new model build fine")
                break
