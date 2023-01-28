#coding=utf-8
import os
import configparser
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def set_config_txt(open_list):
    config_path = "./yolo.txt"
    cf=configparser.ConfigParser()
    cf.read(config_path)
    secs=cf.sections()  # 获得所有区域
    with open(config_path,"w") as f:
        


