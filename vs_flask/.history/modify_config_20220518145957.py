#coding=utf-8
import os
import configparser
import sys
# sys.reload(sys)
# sys.setdefaultencoding("utf-8")


open_list = [["1","https://111"],["2","https://222"]]

num_source = len(open_list)

def set_config_txt(open_list):
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
        # cf.write(f)


