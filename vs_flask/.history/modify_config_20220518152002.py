#coding=utf-8
import os
import configparser
import sys
# sys.reload(sys)
# sys.setdefaultencoding("utf-8")


open_list = [["192.168.21.2","https://111"],["193,423,232,1","https://222"]]

# new_num_source = len(open_list)

def set_config_txt(open_list):
    new_num_source = len(open_list)
    config_path = "./yolo.txt"
    cf=configparser.ConfigParser()
    cf.read(config_path)
    secs=cf.sections()
    with open(config_path,"w") as f:
        old_source = []
        for sec in secs:
            if len(sec) > 5:
                if sec[0:6]=="source":
                    print(sec)
                    old_source.append(sec)
        print(old_source)
        if(new_num_source<len(old_source)):
            for i in range(new_num_source):
                new_sec = "source"+str(i)
                cf.set(new_sec,"enable",1)
                cf.set(new_sec,"enable",1)


set_config_txt(open_list)
