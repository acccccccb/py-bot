# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
# import http.server
import time
import logging
import asyncio
from flask import Flask, Response
import cv2



def http_server(queue):
    HTTP_HOST = os.getenv('HTTP_HOST')
    HTTP_PORT = os.getenv('HTTP_PORT')
    # 将队列对象传递给路由处理程序
    app = Flask(__name__)
    # 禁用开发服务器的警告信息
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    # app.logger.setLevel(logging.ERROR)
    def generate_video(queue):
        if os.getenv('HTTP') == "OPENCV":
            video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (800, 600))
            while True:
                frame = queue.get()  # 从队列中获取视频帧
                video_writer.write(frame)
                yield (b'--frame\r\n' + b'Content-Type: video/mp4\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
        else:
            return "OPENCV NOT RUNNING"

    def generate_image(queue):
        if os.getenv('HTTP') == "OPENCV":
            while True:
                frame = queue.get()  # 从队列中获取视频帧
                _, jpeg = cv2.imencode('.jpg', frame)  # 将帧编码为 JPEG 格式
                yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
                # time.sleep(1/30)
        else:
            return "OPENCV NOT RUNNING"

    @app.route('/')
    def index():
        if os.getenv('HTTP') == "OPENCV":
            return Response(generate_image(queue), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return "OPENCV NOT RUNNING"

    @app.route('/video_feed')
    def video_feed():
        if os.getenv('HTTP') == "OPENCV":
            return Response(generate_video(queue), mimetype='video/mp4')
        else:
            return "OPENCV NOT RUNNING"

    @app.route('/image_feed')
    def image_feed():
        if os.getenv('HTTP') == "OPENCV":
            return Response(generate_image(queue), mimetype='multipart/x-mixed-replace; boundary=frame')
        else:
            return "OPENCV NOT RUNNING"

    print(f"http_server: {HTTP_HOST}:{HTTP_PORT}")
    app.run(HTTP_HOST, int(HTTP_PORT), debug=False)
    
if __name__ == '__main__':
    http_server()