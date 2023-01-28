#coding=utf-8
#author:jzx

#1.说明1.img_list还的生成，确定通道数目
#2.说明2：200是成功，500是失败
#3.说明3：开关还没有实现，添加相机
#4.说明4：关闭rtsp流
#5.说明5. 行为类别定义
#6.说明6：每次消息里面有多个，一张图片里面可能也有多个
#7.说明7.创建一个http服务器，传输图片
#8.说明8.解析删除添加相机
#9.画框+label
#10.画了框在人脸检测吧 ，无所谓了


from ast import arg
from distutils.log import debug
from faulthandler import disable
import os
from pdb import post_mortem
from statistics import mode
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from charset_normalizer import detect
from cv2 import CMP_EQ
from flask import Flask, jsonify, request, current_app, redirect
from flask_sqlalchemy import SQLAlchemy
import click
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
import shutil
from flask_apscheduler import APScheduler
from flask import g
import cv2 
import json
import subprocess
from matplotlib.pyplot import eventplot
import requests
from flask import session
import redis
from modify_config import set_config_txt

#定时服务启动配置参数
class Config(object):
    JOBS = [
        {
            'id': 'send_results',                # 一个标识
            'func': '__main__:send_results',     # 指定运行的函数 
            'trigger': 'interval',       # 指定 定时任务的类型
            'seconds': 1                # 运行的间隔时间
        }
    ]
SCHEDULER_API_ENABLED = True


#redis维护 url池，相机池
globalredisconn = redis.Redis(host='localhost', port=6379, decode_responses=True)


#todo image_list 需要生成
# num_source = 2
# image_list=[]
# for i in range(num_source):
#     txt = "/home/cookoo/images/"+str(i)+"_image.png"
#     image_list.append(txt)


label_dict = {
    "wcaqm",(1002001,"未穿安全帽"),
    "wcgz",(1002002,"未穿工装"),
    "rljc",(1002101,"人脸检测"),
}




def send_results():
    with app.app_context():
        #debug
        clinetlistJson = globalredisconn.get("clinetlist")
        print(clinetlistJson)
        exchange_path = "/home/cookoo/images"
        new_path =  "/home/cookoo/save_result"
        step2_flag ="/home/cookoo/images/flag2.done"
        image_list = ["/home/cookoo/images/0_image.png","/home/cookoo/images/1_image.png"]
        if(os.path.exists(step2_flag)):
            happen_time = time.time()
            time.sleep(0.1)
            detection_results = []
            new_folder = new_path + "/" + str(happen_time)
            for i,p in enumerate(image_list):
                if os.path.exists(p):
                    result={}
                    label_path = "/home/cookoo/images/"+str(i)+"_labels.txt"
                    face_path = "/home/cookoo/images/"+str(i)+"_image_detected.jpg"
                    result["通道"]=i #相机id，
                    result["raw_image"]=p 
                    result["face_image"]=face_path
                    result["detection_result"] =label_path
                    try:
                        img = cv2.imread(face_path)
                        cv2.imshow("face recognition",img)
                        cv2.waitKey(1)
                    except cv2.error as e:
                        print("there is error !")
                    #处理labels数据
                    #处理原始图片数据label_dict
                    #处理人脸检测的数据
                    #在这里要loop label path
                    with open(label_path) as f:
                        lines = f.readlines()
                        for line in lines:
                            eventType = line.split(" ")[0]
                            detection_result = {"ability":"event_frs",
                                    "eventData":"string",
                                    "eventId":"1",
                                    "eventType":label_dict[eventType][0],
                                    "eventTypeName":"安全帽",
                                    "eventVoice":"三号没带安全帽",
                                    "happenTime":happen_time,
                                    "imageUrl":"",
                                    "sendTime":"2022-02-12 19:23:11",
                                    "srcIndex":"dafdafda",
                                    "srcName":"3hao",
                                    "srcNameRe":"mo",
                                    "srcParentIndex":"string",
                                    "srcType":"eventRule",
                                    "status":"0",
                                    "syncDate":"2022-02-12 19:23:11",
                                    "timeOut":"0",
                                    "uids":"string",
                                    "visiblePicUrl":"http://192.168.212.195/file/1652680907.2166882/0_image_detected.jpg"
                                    }
                            detection_results.append(detection_result)
                else:
                    print("该通道未检测到数据")

            # 检测到数据,发送数据
            if(len(detection_results)>1):
                result_json = {"code":0,"data":detection_results,"msg":"成功"}
                #发送结果,将结果写入给服务端
                clientlistJson = globalredisconn.get("clinetlist")
                if clientlistJson is not None:
                    clinetlist = json.loads(clientlistJson)                    
                    for key in clinetlist.keys():
                        send_num = 0
                        while send_num < 3:  # 最大发送次数
                            print('post--clientlist[str(clinet_id)]:', clientlist[str(key)]["url"])
                            r = requests.post("http://192.168.212.101:5000/api/AlarmResult/",json.dumps(result_json))
                            print("向上位机发送结果：", r.text)
                            send_num += 1
                            if (r.status_code == 200):
                                print(u"========发送结果成功")
                                break
                            else:
                                print(u"========发送结果失败")
                                continue
            #保存文件
            files = os.listdir(exchange_path)
            if(len(files)>2):
                shutil.copytree(exchange_path,new_folder)
            # post 写文件
            #清空文件
            for f in files:
                os.remove(exchange_path+"/"+f)
        else:
            temp_list=[]

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string sgai jzx')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.cli.command()
def initdb():
    db.create_all()
    click.echo("Initialized database.")


# Models
class User(db.Model):
    userName = db.Column(db.String(50), primary_key = True)
    userPwd = db.Column(db.Text, nullable=False)


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    #第一个参数是内部的私钥，这里写在共用的配置信息里了
    #第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=None)
    #接收用户id转换与编码
    token = s.dumps({"id":api_user}).decode("ascii")
    print("注册了token")
    print(token)
    return token

def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    #参数为私有秘钥，跟上面方法的秘钥保持一致
    print("验证token")
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        #转换为字典
        data = s.loads(token)
    except Exception:
        return False
    return True


@app.route('/')
def index():
    # us = User.query.all()
    # for u in us:
    #     db.session.delete(u)
    # db.session.commit()
    # clinetlist = dict()
    # clinetlistJson = globalredisconn.get("clinetlist")
    # print("现有的url池clinetlist url ： ",clinetlistJson)
    # if clinetlistJson is not None:
    #     clinetlist = json.loads(clinetlistJson)
    # # 如果池子里面有该链接，就返回
    # for key in clinetlist.items():
    #     if key[1]["url"] == "111":
    #         print("url池子 存在该 url，返回")
    #         break
    # print("添加该url到线程池")
    # post_data = {}
    # post_data["url"] = time.time()
    # post_data["time"] = "23455"
    # aha =time.time()
    # clinetlist[aha] = post_data
    # clinetlistJson = json.dumps(clinetlist)
    # globalredisconn.set("clinetlist",clinetlistJson)

    return '<h1>Hello!<h1>'
#用户注册，保存进数据库
@app.route('/api/user/register', methods=['POST'])
def register():
    userName = request.form.get('userName')
    userPwd = request.form.get('userPwd')
    save = User(userName=userName, userPwd=userPwd)
    db.session.add(save)
    db.session.commit()
    return jsonify('success')

#比对储存的用户返回带有有效期的token
@app.route('/api/user/login', methods=['POST'])
def login():
    print("= =登录 = =")
    temp = request.form.to_dict()
    print(temp)
    userName = temp['userName']
    userPwd = temp['userPwd']
    print(userName)
    print(userPwd)
    u = User.query.filter_by(userName=userName).first()
    if not u:
        return jsonify({"CODE":500,"MESSAGE":None})
    if userPwd == u.userPwd:
        token = create_token(userName) 
        print("= =登录成功 返回token = =")
        return jsonify({"CODE":200,"MESSAGE":token})
    else:
        print("= = 登录失败 = =")
        return jsonify({"CODE":500,"MESSAGE":None})

#接收订阅地址
@app.route('/api/EventReceive/v1.0.0', methods=['POST'])
def Receive():
    print(" = 接收发送过来的地址 = ")
    print(request.form.get)
    receiveid = request.form.get('receiveId')
    receive_url = request.form.get('receive_url')
    if verify_token(receiveid):
        clinetlist = dict()
        post_data = dict()
        #"clinetlist" 是redis中客户端列表
        clinetlistJson = globalredisconn.get("clinetlist")
        print("现有的url池clinetlist url ： ",clinetlistJson)
        if clinetlistJson is not None:
            clinetlist = json.loads(clinetlistJson)
        # 如果池子里面有该链接，就返回
        for key in clinetlist.items():
            if key[1]["url"] == receive_url:
                print("url池子 存在该 url，返回")
                break
        print("添加该url到线程池")
        post_data["url"] = receive_url
        post_data["time"] = time.time()
        clinetlist[str(receiveid)] = post_data
        clinetlistJson = json.dumps(clinetlist)
        globalredisconn.set("clinetlist",clinetlistJson)
        print(receive_url)
        return jsonify({"CODE":200,"MESSAGE":receive_url})
    else:
        print("验证未通过")
        return jsonify({"CODE":500,"MESSAGE":None})

#相机状态设置,设置相机是否可用
@app.route('/api/setCameraStatus', methods=['POST'])
def setCameraStatus():
    print("== 设置相机状态 ==")
    # ImmutableMultiDict([('', '{"items":[{"id":"c202da68-a4d5-4e08-a031-8708b36e806c"}，{"id":"21212-a4d5-4e08-a3232-8708b36e806c"}]}')])>
    #加载当前相机池
    cameralist = dict()
    #"clinetlist" 是redis中客户端列表
    cameralistJson = globalredisconn.get("cameralist")
    if cameralistJson is not None:
        cameralist = json.loads(cameralistJson)
    
    post_get  = request.form.get()
    for i,s in post_get.items():
        dict_info = json.loads(s)
        camera_status_list = dict_info['items']	# print(type(s))
        for item in camera_status_list:
            camera_enable_id = item["id"]
            # 如果池子里面有该链接，就返回
            for item in cameralist.items():
                if item[0] == camera_enable_id:
                    item[1]["enable"] = "1"

    open_list = []
    for item in cameralist.items():
        if(item[1][1]) == "1":
            open_list.append([item[0],item[1,0]]) #一个id ，一个rtsp
    #修改config文件
    set_config_txt(open_list)        
    result = True
    if not result:
        return jsonify({"CODE":500,"MESSAGE":None})
    else:
        return jsonify({"CODE":200,"MESSAGE":None})

#新增加相机接口 -维护相机池//id id是-1的时候，传入的是ip值
@app.route('/api/addCamera', methods=['POST'])
def addCamera():
    print("== 增加相机 ==")
    #<bound method TypeConversionDict.get of ImmutableMultiDict([('', '{"items":[{"content":"轨道机器人1-可见光视频服务器2","ext":null,"user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null}]}')])>
    post_get = request.form.get()
    # 可能不需要loop，i是空，s是{item}
    for i,s in post_get.items():
        dict_info = json.loads(s)
        camera_list = dict_info['items']
        for item in camera_list:
            content = item["content"]
            ext = item["ext"]
            user = item["user"]
            password = item["password"]
            ip = item["ip"]
            port = item["port"]
            options = item["options"]
            id = item["id"]
            rtsp_url = "rtsp://"+str(user)+":"+str(password)+"@"+str(ip)+":"+"port"+str(ext)
            print(rtsp_url)
            #添加相机到相机池
            cameralist = dict()
            cameralistJson = globalredisconn.get("cameralist")
            print("现有的camera list ： ",cameralistJson)
            if cameralistJson is not None:
                cameralist = json.loads(cameralistJson)
            # 如果池子里面有该链接，就返回
            for key in cameralist.items():
                if key[1]["rtsp_url"] == rtsp_url:
                    print("rtsp_url 存在,不添加了，返回")
                    break
            print("添加相机的camera list")
            post_data = {}
            post_data["rtsp"] = rtsp_url
            post_data["enable"] = "0"

    
            cameralist[ip] = post_data
            
            cameralistJson = json.dumps(cameralist)
            globalredisconn.set("cameralist",cameralistJson)
    #就保存内存里
    return jsonify({"CODE":200,"MESSAGE":None})

#删除相机接口 - 去修改yolo.txt 本地也同时维护一下相机列表的list。global
@app.route('/api/deleteCamera', methods=['POST'])
def deteteCamera():
    print(request.form.get)
    modify_yolo_config_txt()
    result = True
    if not result:
        return jsonify({"CODE":500,"MESSAGE":"[1,2,3]"})
    else:
        return jsonify({"CODE":200,"MESSAGE":None})

def modify_yolo_config_txt():
    pass


if __name__=="__main__":
    
    #detection_process = multiprocessing.Process(target = start_deepstream_and_arcface)
    #detection_process.start()
    # start_deepstream()
    # print("11111111111111111")
    #start_arcface()
    
    #0.所有相机关闭
    # 有了修改相机才启动 deepstream 刚开始没数据的话，会不会
    #1.redis 清空
    globalredisconn.flushall()
    
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False,host ='0.0.0.0',use_reloader=False)
