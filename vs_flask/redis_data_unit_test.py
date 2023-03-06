#redis数据定义单元测试


#相机池测试
#数据格式说明

#ip地址是索引，值里面包含网址和状态
# {"192.178.93": {"rtsp": "www.nihaobang.com", "enable": "0"}, "110.42.32": {"rtsp": "www.n\u4e3abang.com", "enable": "1"}}


#姓名是索引，值里面一个网址一个时间，测试通过
#{'laowang': {'url': '123456', 'time': 1653037177.747139}, 'laoliu': {'url': '12345', 'time': 1653037177.7475634}}

import json
import redis

#0.测试相机池
print("--------------测试相机池----------------")
globalredisconn = redis.Redis(host='localhost', port=6379, decode_responses=True)
#加一个数据 add camera
# cameralist = dict()
# post_data = {}
# post_data["rtsp"] = "www.nihaobang.com"
# post_data["enable"] = "0"
# post_data["deepstram_id"] = "0"
# ip = "192.178.93"
# cameralist[ip] = post_data
# cameralistJson = json.dumps(cameralist)
# globalredisconn.set("cameralist",cameralistJson)
# #拿到数据
# cameralist = dict()
# cameralistJson = globalredisconn.get("cameralist")
# if cameralistJson is not None:
#     cameralist = json.loads(cameralistJson)
# print(cameralist)

# #再加一个数据
# post_data = {}
# post_data["rtsp"] = "www.n为bang.com"
# post_data["enable"] = "1"
# post_data["deepstram_id"] = "1"
# ip = "110.42.32"
# cameralist[ip] = post_data
# cameralistJson = json.dumps(cameralist)
# globalredisconn.set("cameralist",cameralistJson)

# #拿到数据
# cameralist = dict()
# cameralistJson = globalredisconn.get("cameralist")
# if cameralistJson is not None:
#     cameralist = json.loads(cameralistJson)

# print(cameralist)
# #遍历得到里面的数据
# for key in cameralist.items():
#     print(key[0])
#     print(key[1]["rtsp"])
#     print(key[1]["enable"])
#     print(key[1]["deepstram_id"])
    

# print("--------------测试链接池----------------")

# clinetlist=dict()

# clinetlistJson = globalredisconn.get("clinetlist")
# print("现有的url池clinetlist url ： ",clinetlistJson)
# if clinetlistJson is not None:
#     clinetlist = json.loads(clinetlistJson)


# receiveid = "laowang"
# receive_url = "123456"

# import time

# # 如果池子里面有该链接，就返回

# post_data = dict()
# post_data["url"] = receive_url
# post_data["time"] = time.time()
# clinetlist[str(receiveid)] = post_data
# clinetlistJson = json.dumps(clinetlist)
# globalredisconn.set("clinetlist",clinetlistJson)

# #测试如果是一样的数据，会不会出错 不会出错
# post_data = dict()
# post_data["url"] = receive_url
# post_data["time"] = time.time()
# clinetlist[str(receiveid)] = post_data
# clinetlistJson = json.dumps(clinetlist)
# globalredisconn.set("clinetlist",clinetlistJson)


# receiveid = "laoliu"
# receive_url = "12345"
# #测试如果是一样的数据，会不会出错 不会出错
# post_data = dict()
# post_data["url"] = receive_url
# post_data["time"] = time.time()
# clinetlist[str(receiveid)] = post_data
# clinetlistJson = json.dumps(clinetlist)
# globalredisconn.set("clinetlist",clinetlistJson)


# clinetlistJson = globalredisconn.get("clinetlist")
# print("现有的url池clinetlist url ： ",clinetlistJson)
# if clinetlistJson is not None:
#     clinetlist = json.loads(clinetlistJson)

# print(clinetlist)

# post_urls = []
# for i in clinetlist.items():
#     post_urls.append(i[1]["url"])

# print(post_urls)

open_list = [["123","156","789"],["789","123","aaa"]]
open_list_json = json.dumps(open_list)
globalredisconn.set("deepstream_id",open_list_json)



deepstream_id = globalredisconn.get("deepstream_id")
print("现有的url池clinetlist url ： ",deepstream_id)
if deepstream_id is not None:
    deepstream_id_list = json.loads(deepstream_id)
    print(deepstream_id_list[0][2])

