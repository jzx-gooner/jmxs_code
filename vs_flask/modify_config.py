#coding=utf-8
# 修改deepstream的config文件
# input：
# output：
import configparser
# sys.reload(sys)
# sys.setdefaultencoding("utf-8")
# new_num_source = len(open_list)

# 永远只开启开启的

def set_config_txt(open_list):
    new_num_source = len(open_list)
    print("open_list的输入是：")
    print(open_list)
    if(new_num_source>0):
        config_path = "/opt/nvidia/deepstream/deepstream-6.0/sources/apps/sample_apps/deepstream-app/config/jmxs.txt"
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
                    cf.set(new_sec,"enable","1")
                    cf.set(new_sec,"uri",str(open_list[i][1]))
                for i in range(new_num_source,old_num_source):
                    new_sec = "source"+str(i)
                    cf.set(new_sec,"enable","0")
                cf.write(f)
            else:
                for i in range(old_num_source):
                    new_sec = "source"+str(i)
                    cf.set(new_sec,"enable","1")
                    cf.set(new_sec,"uri",str(open_list[i][1]))
                for i in range(old_num_source,new_num_source):
                    new_sec = "source"+str(i)
                    has_section = cf.has_section(new_sec)
                    if not has_section:
                        cf.add_section(new_sec) 
                    cf.set(new_sec,"uri",str(open_list[i][1]))
                    cf.set(new_sec,"enable","1")
                    cf.set(new_sec,"type","3")
                    cf.set(new_sec,"num-source","1")
                cf.write(f)
    else:
        print("没有添加数据")
    return
# open_list=[["id","rtsp",'0','ip]]
# set_config_txt(open_list)
