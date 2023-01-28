#测试rtsp流
#coding=utf-8
import cv2
url = "rtsp://admin:12345678a@192.168.33.247:554/Streaming/Channels/1"
cap=cv2.VideoCapture(url)
ret,frame = cap.read()
while ret:
    print(frame)
    #cv2.imshow("frame",frame)
    #cv2.waitKey(1)
cap.release()
