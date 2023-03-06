import sys
import os
import time
from genericpath import exists
from tools import deepstream_status,start_deepstream
work_dir = "/configs_dir"
sys.path.append(work_dir)
exchange_path = work_dir+"/jmxs_images"
new_path =  work_dir+"/jmxs_save_result"
step2_flag =work_dir+"/jmxs_images/flag.txt"
while(1):
    d_s = deepstream_status()
    print("deepstream app status "+ str(d_s))
    if not d_s:
        print("restart deepstream ")
        start_deepstream()
    if(os.path.exists(step2_flag)):
        timeArray = time.localtime(float(time.time())+28800)
        happen_time = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
        name_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        time.sleep(0.1)
        detection_results = []
        new_folder = new_path + "/" + str(name_time)
        num_source =2
        image_list = [work_dir+"/images/"+str(i)+"_image.png" for i in range(0,num_source)]
        for i,p in enumerate(image_list):
            if os.path.exists(p):
                label_path = work_dir+"/images/"+str(i)+"_labels.txt"
                if exists(label_path):
                    print("111111111")
                              
        files = os.listdir(exchange_path)

        for f in files:
            os.remove(exchange_path+"/"+f)
        print("发送结果")
        time.sleep(5)
