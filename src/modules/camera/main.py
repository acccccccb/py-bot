# -*- coding: utf-8 -*-
import json
import os
import cv2
import base64
import asyncio

def video_stream(queue):
    
    # 加载人脸识别模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 加载已知人脸图像
    known_faces_dir = os.path.join(os.getcwd(), 'src', 'modules','camera','known_faces','face_1')
    known_faces = []
    for filename in os.listdir(known_faces_dir):
        image = cv2.imread(os.path.join(known_faces_dir, filename))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            known_faces.append(face)


    # 初始化摄像头
    camera = cv2.VideoCapture(0)
    width = 640
    height = 480
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    async def main():
        while True:
            # 读取摄像头画面
            ret, frame = camera.read()
            frame = cv2.flip(frame, 1)
            # 将帧转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 人脸检测
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
            # 人脸识别
            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                
                # 与已知人脸进行匹配
                match = False
                for known_face in known_faces:
                    # 使用比较函数进行匹配
                    result = cv2.matchTemplate(face, known_face, cv2.TM_CCOEFF_NORMED)
                    if result.all() >= 0.7:
                        match = True
                        break
                
                # 标记人脸及识别结果
                if match:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, 'Match', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, 'Unknown', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            
            # 显示结果
            # cv2.imshow('Face Recognition', frame)
            queue.put(frame)
            # 适当的延迟，控制视频的帧率
            await asyncio.sleep(0.1)
        # 关闭摄像头
        camera.release()

    asyncio.run(main())
