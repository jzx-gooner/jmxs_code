#coding=utf-8
import os
import configparser
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def set_config_txt(camera_dict):
    config_path = "./yolo.txt"
    cf=configparser.ConfigParser()
    cf.read(config_path)
    secs=cf.sections()  # 获得所有区域
    with open(config_path,"w") as f:
        for sec in secs:
            if len(sec) > 5:
                if sec[0:6]=="source":
                    # print(cf.options(sec))
                    print(sec)
                    cf.set(sec,"enable","1")
                    cf.set(sec,"uri","你好啊")
        cf.write(f)


