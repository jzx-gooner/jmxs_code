#时间戳测试
#部分服务器时间不一致问题
import time
timeArray = time.localtime(float(time.time())+28800)
time_style = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
print(time_style)
