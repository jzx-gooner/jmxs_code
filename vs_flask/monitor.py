#coding=utf-8
import os
import time
import cv2
from flask import Flask, render_template, request, send_from_directory,Response
import psutil
import signal
import subprocess
import sys

from tools import kill_deepstream

app = Flask(__name__)

rtsp_url = ""
@app.route('/')
def hello_world():
    return 'Hello World!,this is jmxs monitor'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # 渲染文件
    return render_template('upload.html')


# 文件保存的目录，根据实际情况的文件结构做调整；
# 若不指定目录，可以写成f.save(f.filename)，可以默认保存到当前文件夹下的根目录
# 设置上传文件保存路径 可以是指定绝对路径，也可以是相对路径（测试过）
app.config['UPLOAD_FOLDER'] = '/configs_dir/jmxs_log/'	## 该目录需要自行创建
# 将地址赋值给变量
file_dir = app.config['UPLOAD_FOLDER']

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    """  文件上传  """
    if request.method == 'POST':
        # input标签中的name的属性值
        f = request.files['file']

        # 拼接地址，上传地址，f.filename：直接获取文件名
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        # 输出上传的文件名
        print(request.files, f.filename)

        return '文件上传成功!'
    else:
        return render_template('upload.html')


def start_app():
    a = subprocess.Popen("sh go_app.sh",stdout=sys.stdout,stderr=sys.stderr,shell=True)
    print(a.poll())
    time.sleep(5)
    print(a.poll())
    return
def start_apache2():
    a = subprocess.Popen("sh go_apache2.sh",stdout=sys.stdout,stderr=sys.stderr,shell=True)
    print(a.poll())
    time.sleep(3)
    print(a.poll())
    return


def kill_app():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        try:
            print(p.name())
            if(p.name()=="app.bin"):
                os.kill(pid,signal.SIGKILL)
        except:
            print("wuhu")

@app.route('/download', methods=['GET', 'POST'])
def download():
    """  文件下载  """
    timelist = []  # 获取指定文件夹下文件并显示
    Foder_Name = []  # 文件夹下所有文件
    Files_Name = []  # 文件名

    # 获取到指定文件夹下所有文件
    lists = os.listdir(file_dir + '/')

    # 遍历文件夹下所有文件
    for i in lists:
        # os.path.getatime => 获取对指定路径的最后访问时间
        timelist.append(time.ctime(os.path.getatime(file_dir + '/' + i)))

    # 遍历文件夹下的所有文件
    for k in range(len(lists)):
        # 单显示文件名
        Files_Name.append(lists[k])
        # 获取文件名以及时间信息
        Foder_Name.append(lists[k] + " ~~~~~~~~~~~~~~~~~~~~~ " + timelist[k])

    print(file_dir)  # ./upload

    return render_template('download.html', allname=Foder_Name, name=Files_Name)


@app.route('/downloads/<path:path>', methods=['GET', 'POST'])
def downloads(path):
    """ 下载 """
    """
        重写download方法，根据前端点击的文件传送过来的path，下载文件
		send_from_directory：用于下载文件
		flask.send_from_directory(所有文件的存储目录，相对于要下载的目录的文件名，as_attachment：设置为True是否要发送带有标题的文件)
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], path, as_attachment=True)


@app.route("/debug", methods=['POST', "GET","ACTION"])
def button_t():
    message = ''
    print(request.method)
    if request.method == 'GET':
        return render_template('debug.html', message = '未点击按钮')

    if request.method == "POST":
        user_info = request.form.to_dict()
        global rtsp_url 
        rtsp_url = user_info['rtsp']
        return render_template('rtsp.html')

@app.route("/api/Stopjmxs")
def StopAll():
     print("kill jmxs app")
     kill_deepstream()
     kill_app()
     return ('STOP 静默巡视')
@app.route("/api/Restartjmxs")
def RestartJmxs():
    kill_deepstream()
    kill_app()
    start_app()
    return("restart")

@app.route("/api/AlgState")
def is_jmxs_alive():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        print(p.name())
        if(p.name()=="app.bin"):
            return str({"code":200,"description":"{jmxs:1}"})
    return  ({"code":200,"description":"{jmxs:0}"})


@app.route("/api/deepstreamState")
def is_deepstream_alive():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        print(p.name())
        if(p.name()=="deepstream-app"):
            return str({"code":200,"description":"{deepstream:1}"})
    return  ({"code":200,"description":"{deepstream:0}"})

@app.route("/api/Startjmxs")
def StartJmxs():
    start_app()
    return("start")

@app.route("/api/Startapache2")
def StartApache2():
    start_apache2()
    return("start apache2")

#rstp显示测试功能
def gen_frames():  
	# generate frame by frame from camera
    camera = cv2.VideoCapture(rtsp_url)  
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


"""
    运行项目
"""
if __name__ == '__main__':
    HOST = '0.0.0.0'
    app.run(host=HOST, debug=False,port=5006)
