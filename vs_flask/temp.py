# a = [{'id': 'c202da68-a4d5-4e08-a031-8708b36e806c', 'ip': '192.168.114.210'}]
# for post in a:
#     print(post["ip"])


# import time


# d=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

# print(d)

# def add():
#     global a
#     a=[]
#     a.append("2")

# def add2():
#     global a
#     a=[]
#     a.append("3")

# def use():
#     global a
#     print(a)

# add()
# add2()
# use()
# from email.mime import image

# import time
# image_list = ["/home/cookoo/images/"+str(i)+"_labeled.png" for i in range(0,2)]
# print(image_list)
# new_image_list = [i.replace("labeled",str(time.time())).replace("images",) for i in image_list]
# print(new_image_list)
    # for s,t in zip(image_list,new_image_list):
    #     shutil.copy(s,t)

import time

print(str(time.time().as_integer_ratio))
