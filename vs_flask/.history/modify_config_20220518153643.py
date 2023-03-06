#coding=utf-8
import os
import configparser
import sys
# sys.reload(sys)
# sys.setdefaultencoding("utf-8")
# new_num_source = len(open_list)

def set_config_txt(open_list):
    new_num_source = len(open_list)
    config_path = "./yolo.txt"
    cf=configparser.ConfigParser()
    cf.read(config_path)
    secs=cf.sections()
    old_source = []
    for sec in secs:
        if len(sec) > 5:
            if sec[0:6]=="source":
                print(sec)
                old_source.append(sec)
    old_num_source = len(old_source)
    with open(config_path,"w") as f:
        if(new_num_source<=old_num_source):
            for i in range(new_num_source):
                new_sec = "source"+str(i)
                print(new_sec)
                cf.set(new_sec,"enable","1")
                cf.set(new_sec,"uri",str(open_list[i][1]))
            cf.write(f)
        else:
            for i in range(old_num_source):
                new_sec = "source"+str(i)
                print(new_sec)
                cf.set(new_sec,"enable","1")
                cf.set(new_sec,"uri",str(open_list[i][1]))
            for i in range(old_num_source,new_num_source):
                print(i)
                new_sec = "source"+str(i)
                print(new_sec)
                cf.add_section(new_sec) 
                cf.set(new_sec,"enable","1")
                cf.set(new_sec,"type","3")
                cf.set(new_sec,"num-source","1")
            cf.write(f)
