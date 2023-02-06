#coding=utf-8
#条件说明：
# 0.仅支持确定路数，本程序限定为4路，且仅可以为rtsp流
# 1.client端 输入为 [url1:1,url2:1,url3:0,url4:1] 1为开启rtsp推流


import ctypes
import configparser



so = ctypes.CDLL("../deepstream-test5-analytics.so")

def modify_the_config():
    print("modify the config")

#run
def basic():
    so.main.restype=None
    so.main.argtypes=ctypes.c_int,ctypes.POINTER(ctypes.c_char_p)
    args = (ctypes.c_char_p*3)(b'../deepstream-test5-analytics',b'-c',b'yolo.txt')
    so.main(len(args),args)
#modify the rtsp

def stop():
    print("stop")

def restart():
    print("restart")




#返回当前推理的所有rtsp流
def get_sources():
    return ["url1",'url2',"url3"]

#根据传入选择的流，展开推流
def choose_rtsp():
    # modify config
    config = configparser.ConfigParser()
    config.read("./yolo.txt")
    # with open("./yolo.txt","w+") as f:
    print(config.sections())
    config.set("sink2","enable","1")
    with open("./yolo.txt","w+") as f:
        config.write(f)
    #kill 
    #restrat
    basic()

#
def get_people():
    print("1111")
# choose_rtsp()