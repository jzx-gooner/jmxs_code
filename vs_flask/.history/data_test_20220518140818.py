from  werkzeug.datastructures import ImmutableMultiDict
import json
#添加相机消息解析测试
a =ImmutableMultiDict([('', '{"items":[{"content":"轨道机器人1-可见光视频服务器1","ext":"/nihao","user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null},{"content":"轨道机器人2-可见光视频服务器2","ext":null,"user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null}]}')])
for i,s in a.items():
    # 可能不需要loop，i是空，s是{item}
    dict_info = json.loads(s)
    camera_list = dict_info['items']	# print(type(s))
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

#设置相机参数解析
b =ImmutableMultiDict([('', '{"items":[{"id":"c202da68-a4d5-4e08-a031-8708b36e806c"},{"id":"21212-a4d5-4e08-a3232-8708b36e806c"}]}')])
for i,s in b.items():
    print(type(s))
    # 可能不需要loop，i是空，s是{item}
    dict_info = json.loads(s)
    camera_list = dict_info['items']	# print(type(s))