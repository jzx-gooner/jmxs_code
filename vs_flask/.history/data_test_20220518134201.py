from  werkzeug.datastructures import ImmutableMultiDict #导入这个模块
a =ImmutableMultiDict([('', '{"items":[{"content":"轨道机器人1-可见光视频服务器2","ext":null,"user":"admin","password":"sgai123456","ip":"192.168.212.62","port":"8000","options":"[{\\"type\\":\\"1001005\\",\\"value\\":\\"图像过暗\\"},{\\"type\\":\\"1001002\\",\\"value\\":\\"黑屏\\"}]","id":null}]}')])

temp = a.to_dict()
print(type(temp))