# 服务端的测试代码
import requests
import time
url_login = 'http://127.0.0.1:5000/api/user/login'
url_register = 'http://127.0.0.1:5000/api/user/register'
# for i in range(1,6):
#     resp_r = requests.post(url_register, {
#         'userName':f'user{i}',
#         'userPwd':'123456'
#     })
#     # resp_l = requests.post(url_login, {
#     #     'userName':'test',
#     #     'userPwd':'test123456'
#     # })
#     print(resp_r.text)

resp_l = requests.post(url_login, {
    'userName':'user1',
    'userPwd':'123456'
})
print(resp_l.text)

while(1):
    resp_t = requests.post('http://127.0.0.1:5000/api/EventReceive/v1.0.0',
        data={
            'receiveid': resp_l.json()['token'],
            'receive_url':'http://127.0.0.1:5000/api/LnintWebServices/AlarmNotify'
        })
    print(resp_t.text)
    time.sleep(2)
