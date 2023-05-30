# -*- coding: utf-8 -*-
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import json
import os
import cv2
import base64
import asyncio
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import face_recognition
import glob
from datetime import datetime
import uuid
import time
import threading
from multiprocessing import Process, Queue
import math


def video_stream(queue):
    global last_save_time
    global known_face_encodings
    global lock
    unknown_face_sub_dir = os.path.join(os.getcwd(), 'src', 'modules',
                                        'camera', 'unknown_faces')
    known_face_sub_dir = os.path.join(os.getcwd(), 'src', 'modules', 'camera',
                                      'known_faces', '*')
    known_face_encodings = []  #已知人脸 编码
    known_face_labels = []  # 已知人脸标签 就是文件夹名称
    tolerance = float(os.getenv('TOLERANCE'))  # 匹配宽容度 0 - 1
    auto_save_unknown_face = os.getenv('AOTO_SAVE_UNKNOWN_FACE')  # 是否自动保存未知人脸
    auto_save_unknown_face_interval = int(
        os.getenv('AOTO_SAVE_UNKNOWN_FACE_INTERVAL'))  # 未知人脸保存间隔 秒
    last_save_time = time.time()

    # 创建一个线程锁，用于线程间的同步
    lock = threading.Lock()

    # 使用 glob.glob 获取所有子文件夹的路径列表
    sub_dirs = glob.glob(known_face_sub_dir)

    # 读取字体文件
    font_path = os.path.join(os.getcwd(), 'src', 'font', 'msyhl')
    font = ImageFont.truetype(font_path, 15)

    def loadFace(known_faces_dir):
        print(f"正在加载人脸图像... {os.path.basename(known_faces_dir)}")
        known_face_encodings = []
        # 加载已知人脸图像
        # 获取文件夹中所有以.jpg或.png结尾的文件路径
        image_files = glob.glob(known_faces_dir +
                                "/*.jpg") + glob.glob(known_faces_dir +
                                                      "/*.png")

        # 遍历图片文件路径并读取人脸编码
        for image_file in image_files:
            # 加载图片文件
            image = face_recognition.load_image_file(image_file)

            # 获取人脸编码
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                face_encoding = face_recognition.face_encodings(image)[0]
                # 将人脸编码添加到已知人脸编码列表中
                known_face_encodings.append(face_encoding)

        return known_face_encodings

    def drawText(text, x, y, draw):
        font_color = (0, 0, 0)  # 字体
        stroke_color = (255, 255, 255)  # 描边
        stroke_width = 1

        draw.text((x - 1, y),
                  text,
                  font=font,
                  fill=stroke_color,
                  stroke_width=stroke_width)
        draw.text((x + 1, y),
                  text,
                  font=font,
                  fill=stroke_color,
                  stroke_width=stroke_width)
        draw.text((x, y - 1),
                  text,
                  font=font,
                  fill=stroke_color,
                  stroke_width=stroke_width)
        draw.text((x, y + 1),
                  text,
                  font=font,
                  fill=stroke_color,
                  stroke_width=stroke_width)
        draw.text((x, y), text, font=font, fill=font_color)

    def appendQueue(q, data):
        if q.full():
            q.get()
        q.put(data)

    def save_unknown_face(frame, y, h, x, w):
        global last_save_time
        # 获取当前时间戳
        current_time = time.time()

        # 判断是否满足保存间隔条件
        if current_time - last_save_time >= auto_save_unknown_face_interval:
            # 根据人脸区域的坐标从原始视频帧中提取人脸区域图像
            face_region = frame[(y - 20):(h + 20), (x - 20):(w + 20)]
            # 生成文件名：日期+UUID
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{now}_{unique_id}.jpg"
            # 构造保存路径
            save_path = os.path.join(unknown_face_sub_dir, filename)
            cv2.imwrite(save_path, face_region)
            last_save_time = current_time

    def match_faces(index, known_face_encoding, face_encoding, tolerance,
                    face_queue):
        global lock
        matches = face_recognition.compare_faces(known_face_encoding,
                                                 face_encoding, tolerance)
        data = {'index': index, 'match': not False in matches}
        with lock:
            face_queue.put(data)

    if len(sub_dirs) == 0:
        print("known_faces文件夹是空的")
        return

    for sub_dir in sub_dirs:
        known_face_encodings.append(loadFace(sub_dir))
        known_face_labels.append(os.path.basename(sub_dir))
    else:
        print("known_faces加载完毕")

    async def main():
        global known_face_encodings

        # 初始化摄像头
        video_path = os.path.join(os.getcwd(), 'src', 'modules', 'camera',
                                  'test_video', 'lei2.mp4')
        camera = cv2.VideoCapture(video_path)
        # camera = cv2.VideoCapture(0)

        # 检查是否成功打开摄像头
        if not camera.isOpened():
            print("无法打开摄像头")
            return

        # 获取宽度和高度
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        maxWidth = 640
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # 获取摄像头的帧率
        fps = camera.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 10

        print(f"摄像头帧率: {fps}")
        print(f"分辨率: {width} x {height}")
        print(f"检测中...")

        while True:
            if not camera.isOpened():
                print(f"camera传入数据为空")
                break
            # 读取摄像头画面
            success, frame = camera.read()

            if not success:
                break

            # frame = cv2.resize(frame, (maxWidth, math.floor(height / (width / maxWidth))))
            frame = cv2.flip(frame, 1)
            # 将视频帧转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 创建可绘制的图像对象
            pil_image = Image.fromarray(rgb_frame)
            draw = ImageDraw.Draw(pil_image)

            # 检测当前帧中的人脸
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_frame, face_locations)

            print(f'检测到人脸数：{len(face_encodings)}')
            if len(face_encodings) > 0:
                # 对每个检测到的人脸进行匹配
                for face_encoding_index, face_encoding in enumerate(
                        face_encodings):
                    y, w, h, x = face_locations[face_encoding_index]
                    # save_unknown_face(frame, y, h, x, w)
                    match = False
                    text = '未知'

                    # 创建线程，并分配人脸编码进行匹配
                    threads = []
                    results = []
                    face_queue = Queue()
                    for i, known_face_encoding in enumerate(
                            known_face_encodings):
                        thread = threading.Thread(target=match_faces,
                                                  args=(i, known_face_encoding,
                                                        face_encoding,
                                                        tolerance, face_queue))
                        threads.append(thread)
                        thread.start()
                    # 等待所有线程执行完毕
                    for thread in threads:
                        thread.join()
                        data = face_queue.get()
                        results.append(data)

                    for result in results:
                        if result.get('match', False) == True:
                            # 如果匹配成功，标记人脸并显示名字
                            text = known_face_labels[result.get('index')]
                            print(f"匹配成功 {text}")
                        else:
                            if auto_save_unknown_face == 'True':
                                save_unknown_face(frame, y, h, x, w)

                    drawText(text, x, y - 20, draw)
                    draw.rectangle([(x, y), (w, h)], outline="white")

                output_frame = cv2.cvtColor(np.array(pil_image),
                                            cv2.COLOR_RGB2BGR)
                appendQueue(queue, output_frame)

                if os.getenv('SHOW_OPENCV_WINDOW') == "True":
                    cv2.imshow("Face Recognition", output_frame)
                    # 等待键盘输入，根据需要进行处理
                    key = cv2.waitKey(1)
                    # 按下空格键退出循环
                    if key == 32:
                        break

                await asyncio.sleep(2 / fps)

                # cv2.imshow("Face Recognition", output_frame)
                # cv2.waitKey(1)
                # await asyncio.sleep(0.1)
            else:
                appendQueue(queue, frame)
                if os.getenv('SHOW_OPENCV_WINDOW') == "True":
                    cv2.imshow("Face Recognition", frame)
                    key = cv2.waitKey(1)
                    # 按下空格键退出循环
                    if key == 32:
                        break

                await asyncio.sleep(1)

        # 关闭窗口
        if os.getenv('SHOW_OPENCV_WINDOW') == "True":
            cv2.destroyAllWindows()
        # 关闭摄像头
        camera.release()

    asyncio.run(main())
