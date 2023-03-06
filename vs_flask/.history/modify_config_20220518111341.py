#coding=utf-8
import os
import configparser

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

config_path = "./yolo.txt"
cf=configparser.ConfigParser()
cf.read(config_path)
secs=cf.sections()  # 获得所有区域



# opts=cf.options("sec_a")  # 获取区域的所有key
# print(opts)

#打印出每个区域的所有属性
with open(config_path,"w") as f:
    for sec in secs:
        if len(sec) > 5:
            if sec[0:6]=="source":
                # print(cf.options(sec))
                print(sec)
                cf.set(sec,"enable","1")
                cf.set(sec,"uri","你好啊")
    cf.write(f)



# items = cf.items("sec_a")  # 获取键值对
# print(items)

# val=cf.get("sec_a","a_key1")
# print(val)  # 20
# print(type(val))  #--><class 'str'>

# val=cf.getint("sec_a","a_key1")
# print(val)  # 20
# print(type(val))  #--><class 'int'>
 
# #设置
# cf.set("sec_b","b_key3","newvalue")
# cf.add_section("newsection")
# cf.set("newsection","new_key","new_value")
 
#写入
# cf.write(open("data.txt","w"))
 
#判断
# ret=cf.has_section("newsection") #判断存不存在
# print(ret)  # True
# cf.remove_section("newsection")#删除

# ret=cf.has_section("newsection") #判断存不存在
