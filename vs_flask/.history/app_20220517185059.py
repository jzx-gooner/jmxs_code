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
import os
from statistics import mode
import sys
from apscheduler.schedulers.background import BackgroundScheduler
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
import requests



class Config(object):
    JOBS = [
        {
            'id': 'get_results',                # 一个标识
            'func': '__main__:get_results',     # 指定运行的函数 
            'trigger': 'interval',       # 指定 定时任务的类型
            'seconds': 1                # 运行的间隔时间
        }
    ]

SCHEDULER_API_ENABLED = True

#todo image_list 需要生成
# num_source = 2
# image_list=[]
# for i in range(num_source):
#     txt = "/home/cookoo/images/"+str(i)+"_image.png"
#     image_list.append(txt)



temp_list=[]
def get_results():
    with app.app_context():
        global temp_list
        exchange_path = "/home/cookoo/images"
        new_path =  "/home/cookoo/save_result"
        step2_flag ="/home/cookoo/images/flag2.done"
        image_list = ["/home/cookoo/images/0_image.png","/home/cookoo/images/1_image.png"]
        if(os.path.exists(step2_flag)):
            time.sleep(0.1)
            temp_list=[]
            for i,p in enumerate(image_list):
                # print(p)
                if os.path.exists(p):
                    result={}
                    #还会存在检测不到人脸的情况，要规避
                    label_path = "/home/cookoo/images/"+str(i)+"_labels.txt"
                    face_path = "/home/cookoo/images/"+str(i)+"_image_detected.jpg"
                    result["通道"]=i
                    result["raw_image"]=p
                    result["face_image"]=face_path
                    result["detection_result"] =label_path
                    temp_list.append(result)
                    try:
                        img = cv2.imread(face_path)
                        cv2.imshow("face recognition",img)
                        cv2.waitKey(1)
                    except cv2.error as e:
                        print("there is error !")
                    #处理labels数据
                    #处理原始图片数据
                    #处理人脸检测的数据
                else:
                    print("该通道未检测到数据")

            #保存文件
            files = os.listdir(exchange_path)
            if(len(files)>2):
                ticks = time.time()
                new_folder = new_path + "/" + str(ticks)
                shutil.copytree(exchange_path,new_folder)
            # post 写文件
            #清空文件
            for f in files:
                os.remove(exchange_path+"/"+f)
        else:
            temp_list=[]
        #在这里发送结果,将结果写入给服务端

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
    g.publish_url = None
    return '<h1>Hello!<h1>'
s
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
    print("登录")
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
        return jsonify({"CODE":200,"MESSAGE":token})
    else:
        return jsonify({"CODE":500,"MESSAGE":None})

#返回带有token的订阅地址
@app.route('/api/EventReceive/v1.0.0', methods=['POST'])
def Receive():
    global publish_url
    print("返回token地址")
    print(request.form.get)
    receiveid = request.form.get('receiveId')
    receive_url = request.form.get('receive_url')
    if verify_token(receiveid):
        # return_url =  redirect(receive_url+'/'+receiveid)
        print("验证通过，返回url")
        print(receive_url)
        g.publish_url = receive_url
        print(g.publish_url)
        return jsonify({"CODE":200,"MESSAGE":receive_url})
    else:
        return jsonify({"CODE":500,"MESSAGE":None})

#返回结果 需要一个global 的 url
@app.route('/api/AlarmNotify/')
def AlarmNotify():
    print("返回结果")
    # print(temp_list)
    print("token 验证成功")
    return jsonify({"code":0,"data":[],"msg":"成功"})

#相机状态设置,设置相机是否可用
@app.route('/api/setCameraStatus', methods=['POST'])
def setCameraStatus():
    print("设置相机")
    print(request.form.get)
    cmdindex = request.form.get('CmdIndex')
    taskid = request.form.get('TaskID')
    cameralist = request.form.get("CameraList")
    result = True
    if not result:
        return jsonify({"CODE":500,"MESSAGE":None})
    else:
        return jsonify({"CODE":200,"MESSAGE":None})

#新增加相机接口 - 去修改yolo.txt
@app.route('/api/addCamera', methods=['POST'])
def addCamera():
    print("增加相机")
    #<bound method TypeConversionDict.get of ImmutableMultiDict([('', '{"items":[{"content":"轨道机器人1-可见光视频服务器2","ext":null,"user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null}]}')])>
    # ImmutableMultiDict([('', '{"items":[{"id":"c202da68-a4d5-4e08-a031-8708b36e806c"}]}')])>
    #全部添加[1,2,3,4] -> [1,2,3,4] todo :替换

    print(request.form.get)
    print(request.form.get[1])
    content = request.form.get('content')
    id = request.form.get('id')
    ext = request.form.get('ext')
    user = request.form.get('user')
    password = request.form.get('password')
    ip = request.form.get('ip')
    port = request.form.get('port')
    options = request.form.get('options')

    result = True
    if not result:
        return jsonify({"CODE":500,"MESSAGE":"[1,2,3]"})
    else:
        return jsonify({"CODE":200,"MESSAGE":None})

#删除相机接口 - 去修改yolo.txt
@app.route('/api/deleteCamera', methods=['POST'])
def deteteCamera():
    print("删除相机")
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
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False,host ='0.0.0.0',use_reloader=False)
    
        
