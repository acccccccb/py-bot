# -*- coding: utf-8 -*-
import os
# import http.server
import asyncio
from flask import Flask, Response
import cv2


def video_server(queue):
    HTTP_HOST = os.getenv('HTTP_HOST')
    HTTP_PORT = os.getenv('HTTP_PORT')
    # 将队列对象传递给路由处理程序
    app = Flask(__name__)

    def generate_video(queue):
        video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (800, 600))
        while True:
            frame = queue.get()  # 从队列中获取视频帧
            video_writer.write(frame)
            yield (b'--frame\r\n' + b'Content-Type: video/mp4\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')


    def generate_image(queue):
        while True:
            frame = queue.get()  # 从队列中获取视频帧
            _, jpeg = cv2.imencode('.jpg', frame)  # 将帧编码为 JPEG 格式
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


    @app.route('/')
    def index():
        return "Video Streaming Server"

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_video(queue), mimetype='video/mp4')

    @app.route('/image_feed')
    def image_feed():
        return Response(generate_image(queue), mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(HTTP_HOST, int(HTTP_PORT))

if __name__ == '__main__':
    video_server()