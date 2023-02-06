#coding=utf-8
#author:jzx
#1：return：ok（200），fail（500） √
#2：heart beat：5min
import os
from socket import IPPROTO_EON
import sys
import time
import cv2 
import json
import subprocess
import requests
import redis
import click
from distutils.command.build_clib import build_clib
from genericpath import exists
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request, current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_apscheduler import APScheduler

from modify_config import set_config_txt
from tools import kill_arcface, kill_deepstream, start_deepstream, start_redis_server,draw_bounding_box,build_engine
from simple_log import Logger
# docker映射文件夹
work_dir = "/configs_dir"
sys.path.append(work_dir)
from config_app import ip_string,port_string,iterval_time,user_confidence,iou_nms

label_type_dict = {"wcaqm":"1002001","wcgz":"1002002","rljc":"333","gz_gray":"111","gz_blue":"2222",}
label_name_dict = {"wcaqm":"未穿安全帽","wcgz":"未穿工装","rljc":"人员倒地","gz_gray":"灰色工装","gz_blue":"蓝色工装",}
focus_type=["wcaqm","wcgz"]

#参数配置说明
function_method = "__main__:send_results"
#1.定时服务启动配置参数
class Config(object):
    JOBS = [
        {
            'id': 'function_method',     # 一个标识
            'func': function_method,     # 指定运行的函数 
            'trigger': 'interval',       # 指定 定时任务的类型
            'seconds': iterval_time      # 运行的间隔时间
        }
    ]
SCHEDULER_API_ENABLED = True


#2.redis维护 url池，相机池
globalredisconn = redis.Redis(host='localhost', port=6379, decode_responses=True)



#4.加载lo
log_time = time.localtime(float(time.time())+28800)
log_name = time.strftime("%Y-%m-%d %H:%M:%S",log_time)
logpath = "/configs_dir/jmxs_log/"+log_name+".txt"
log = Logger(logpath, level='info')
log.logger.info('==={}===\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def send_results():
    with app.app_context():
        #debug
        exchange_path = work_dir+"/jmxs_images"
        new_path =  work_dir+"/jmxs_save_result"
        step2_flag =work_dir+"/jmxs_images/flag.txt"
        clientlistJson = globalredisconn.get("clientlist")
        print("====0.现有的client list====")
        print(clientlistJson)
        log.logger.info('===现有的client list ===: {}\n'.format(clientlistJson))
        #加载当前的相机池
        cameralist = dict()
        cameralistJson = globalredisconn.get("cameralist")
        if cameralistJson is not None:
            cameralist = json.loads(cameralistJson)
        print("===1.现有的camrea list ==== ")
        print(cameralist)

        print("===2.参与静默巡视的相机===")
        deepstream_id_list = []
        deepstream_id = globalredisconn.get("deepstream_id")
        print(deepstream_id)
        if deepstream_id is not None:
            deepstream_id_list = json.loads(deepstream_id)


        num_source = len(deepstream_id_list)
        log.logger.info('参与静默巡视的相机 : {}\n'.format(num_source))
        image_list = [work_dir+"/jmxs_images/"+str(i)+"_image.png" for i in range(0,num_source)]
        if(os.path.exists(step2_flag)):
            timeArray = time.localtime(float(time.time())+28800)
            happen_time = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
            name_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            time.sleep(0.1)
            detection_results = []
            new_folder = new_path + "/" + str(name_time)
            for i,p in enumerate(image_list):
                if os.path.exists(p):
                    label_path = work_dir+"/jmxs_images/"+str(i)+"_labels.txt"
                    if exists(label_path):
                        save_jpg_name = draw_bounding_box(label_path)
                        visiblePicUrl = ip_string+ save_jpg_name.split('/')[-1]
                        print(visiblePicUrl)
                        with open(label_path) as f:
                            lines = f.readlines()
                            for line in lines:
                                eventType = line.split(" ")[0]
                                print("---------------------")
                                print(eventType)
                                if eventType in focus_type:
                                    detection_result = {"ability":"event_frs",
                                            "eventData":"string",
                                            "eventId":"1",
                                            "eventType":label_type_dict[str(eventType)],
                                            "eventTypeName":label_name_dict[str(eventType)],
                                            "eventVoice":"",
                                            "happenTime":happen_time,
                                            "imageUrl":"",
                                            "sendTime":happen_time,
                                            "srcIndex":deepstream_id_list[i][0], #open_list=[["id","rtsp",'0','ip]]
                                            "srcName":"",
                                            "srcNameRe":"",
                                            "srcParentIndex":"string",
                                            "srcType":"eventRule",
                                            "status":"0",
                                            "syncDate":happen_time,
                                            "timeOut":"0",
                                            "uids":"string",
                                            "visiblePicUrl":visiblePicUrl
                                            }
                                    detection_results.append(detection_result)
                                
                     
            files = os.listdir(exchange_path)

            for f in files:
                os.remove(exchange_path+"/"+f)
            # 检测到数据,发送数据
            print("准备发送数据")
            print(detection_results)
            if(len(detection_results)>0):
                print("发送数据")
                log.logger.info('发送数据 n')
                result_json = {"code":0,"data":detection_results,"msg":"成功"}
                #发送结果,将结果写入给服务端
                if clientlistJson is not None:
                    clientlist = json.loads(clientlistJson)                   
                    for key in clientlist.keys():
                        print('post--clientlist[str(client_id)]:', clientlist[str(key)]["url"]) #"http://192.168.212.101:5000/api/AlarmResult/"
                        log.logger.info('post--clientlist: {}'.format(clientlist[str(key)]["url"]))
                        old_time = time.time()
                        r = requests.post(clientlist[str(key)]["url"],json.dumps(result_json),timeout=5)
                        current_time = time.time()
                        print("post运行时间为 ： " + str(current_time - old_time) + "s")
                        if (r.status_code == 200):
                            print(u"========发送结果成功")
                        else:
                            print(u"========发送结果失败")


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
    return '<h1>welcome to sgai jmxs!<h1>'
    
#用户注册，保存进数据库
@app.route('/api/user/register', methods=['POST'])
def register():
    print("== 注册 ==")
    log.logger.info("== 注册 ==")
    userName = request.form.get('userName')
    userPwd = request.form.get('userPwd')
    save = User(userName=userName, userPwd=userPwd)
    db.session.add(save)
    db.session.commit()
    return jsonify('success')

#比对储存的用户返回带有有效期的token
@app.route('/api/user/login', methods=['POST'])
def login():
    log.logger.info("== 登录 ==")
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
    print(" = 接收发送过来的地址,这个地址写数据的时候用 = ")
    log.logger.info(" = 接收发送过来的地址,这个地址写数据的时候用 = ")
    print(request.form.get)
    receiveid = request.form.get('receiveId')
    receive_url = request.form.get('receive_url')
    if verify_token(receiveid):
        clientlist = dict()
        #"clientlist" 是redis中客户端列表
        clientlistJson = globalredisconn.get("clientlist")
        print("现有的url池clientlist url ： ",clientlistJson)
        if clientlistJson is not None:
            clientlist = json.loads(clientlistJson)
            #添加链接
            for key in clientlist.items():
                if key[1]["url"] != receive_url:
                    print("url 不存在,我要添加了")
                    post_data = dict()
                    post_data["url"] = receive_url
                    post_data["time"] = time.time()
                    clientlist[str(receiveid)] = post_data
                    clientlistJson = json.dumps(clientlist)
                    globalredisconn.set("clientlist",clientlistJson)
        else:
            print("我要添加了url 0-1")
            post_data = dict()
            post_data["url"] = receive_url
            post_data["time"] = time.time()
            clientlist[str(receiveid)] = post_data
            clientlistJson = json.dumps(clientlist)
            globalredisconn.set("clientlist",clientlistJson)
        return jsonify({"CODE":200,"MESSAGE":receive_url})
    else:
        print("验证未通过")
        return jsonify({"CODE":500,"MESSAGE":None})

#相机状态设置,设置相机是否可用
#{'data': '{"CmdIndex":"0","TaskID":"","IsUse":"1","CameraList":[{"id":"c202da68-a4d5-4e08-a031-8708b36e806c","ip":"192.168.212.62"}]}'}
@app.route('/api/setCameraStatus', methods=['POST'])
def setCameraStatus():
    print("== 设置相机状态 ==")
    log.logger.info('设置相机状态') 
    #加载当前相机池
    cameralist = dict()
    #"clientlist" 是redis中客户端列表
    cameralistJson = globalredisconn.get("cameralist")
    if cameralistJson is not None:
        cameralist = json.loads(cameralistJson)
    else:
        print("相机池里面没有相机，请先添加相机")
        log.logger.info('相机池里面没有相机，请先添加相机')
        return jsonify({"CODE":500,"MESSAGE":"please add camera before set camera"})
    print("数据库里面的相机list")
    print(cameralist)
    log.logger.info('数据库里面的相机list : {}\n'.format(cameralist))
    post_get = request.form.get('data')
    post_get = json.loads(post_get)
    print("post_get")
    print(post_get)
    log.logger.info('post_get : {}\n'.format(post_get))
    enable = post_get["IsUse"]
    print(enable)
    post_cameralist = post_get["CameraList"]
    print(post_cameralist)

    for key in cameralist.items():
        for post in post_cameralist:
            if key[0] == post["id"]:
                print("在相机池子里找到了该相机ID，给他设置相机状态")
                log.logger.info("数据库里面的相机list")
                post_data = dict()
                post_data["rtsp"] = key[1]["rtsp"]
                post_data["enable"] = enable
                post_data["ip"] = key[1]["ip"]
                cameralist[key[0]] = post_data
                cameralistJson = json.dumps(cameralist)
                globalredisconn.set("cameralist",cameralistJson)
    global open_list
    open_list = []
    print("--------统计更新的cameralist，进入deepstram的config ，永远是开启的-----------")
    print(cameralist)

    #"clientlist" 是redis中客户端列表
    cameralistJson = globalredisconn.get("cameralist")
    if cameralistJson is not None:
        cameralist = json.loads(cameralistJson)

    for item in cameralist.items():
        if(item[1]["enable"]) == "1":
            open_list.append([item[0],item[1]["rtsp"],item[1]["enable"]]) #一个id ，一个rtsp

    if(len(open_list))>0: #只有在有相机的时候才启动deepstream
        #添加数据库
        print("添加deepstram id pool")
        open_list_json = json.dumps(open_list)
        globalredisconn.set("deepstream_id",open_list_json)

        print("关闭deepstream")
        kill_deepstream()
        # print("修改config文件")
        set_config_txt(open_list)
        #todo 重新启动deepstream
        start_deepstream()
    return jsonify({"CODE":200,"MESSAGE":None})

#新增加相机接口 -维护相机池//id id是-1的时候，传入的是ip值
@app.route('/api/addCamera', methods=['POST'])
def addCamera():
    print("== 增加相机 ==")
    #<bound method TypeConversionDict.get of ImmutableMultiDict([(data, '{"items":[{"content":"轨道机器人1-可见光视频服务器2","ext":null,"user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null}]}')])>
    post_get = request.form.to_dict()
    print("接收到的数据")
    print(post_get)
    log.logger.info('增加相机 接收到的数据 : {}\n'.format(post_get))

    for i,s in post_get.items():
        dict_info = json.loads(s)
        post_list = dict_info['items']
        
        #加载当前的相机池
        cameralist = dict()
        cameralistJson = globalredisconn.get("cameralist")
        print("现有的camera list ： ",cameralistJson)
        log.logger.info('现有的camera list  : {}\n'.format(cameralistJson))
        if cameralistJson is not None:
            cameralist = json.loads(cameralistJson)

        for item in post_list:
            content = item["content"]
            ext = item["ext"]
            user = item["user"]
            password = item["password"]
            ip = item["ip"]
            port = item["port"]
            options = item["options"]
            id = item["id"]
            rtsp_url = "rtsp://"+str(user)+":"+str(password)+"@"+str(ip)+":"+port+"/Streaming/Channels/1"
            print(rtsp_url)
            print("添加相机的camera list，以ID为key")
            post_data = {}
            post_data["rtsp"] = rtsp_url
            post_data["enable"] = "0"
            post_data["ip"] = ip
            cameralist[id] = post_data
            cameralistJson = json.dumps(cameralist)
            globalredisconn.set("cameralist",cameralistJson)
    #就保存内存里
    return jsonify({"CODE":200,"MESSAGE":None})

#删除相机接口 - 去修改yolo.txt 本地也同时维护一下相机列表的list。global
@app.route('/api/deleteCamera', methods=['POST'])
def deteteCamera():
    print(request.form.get)
    result = True
    if not result:
        return jsonify({"CODE":500,"MESSAGE":None})
    else:
        return jsonify({"CODE":200,"MESSAGE":None})


#每5min接收一次，返回结果
@app.route('/api/KeepAlive', methods=['POST'])
def heartBeat():
    print("== heart beat ==")
    log.logger.info('== heart beat ==')
    token = request.form.get("Token")
    return jsonify({"CODE":200,"MESSAGE":None})



if __name__=="__main__":
    print("0.解密模型，编译生成engine")
    build_engine()
    print("1.开启，并且清空redis数据库")
    start_redis_server()
    globalredisconn.flushall()
    print("2.启动定时服务")
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.start()
    print("3.启动flask")
    app.run(debug=False,host ='0.0.0.0',port=port_string,use_reloader=False)
