# -*- coding: utf-8 -*-
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import os
import signal
import subprocess
import asyncio
import time
import threading
from multiprocessing import Process, Queue
from typing import Any
# from src.modules.speak.main import speak
from src.modules.gamepad.main import gamepad
from src.modules.socket.main import start_websocket
from src.modules.web.main import http_server
from src.modules.camera.main import video_stream
from src.modules.lcd.main import lcd_driver

# 创建队列用于存储输出结果
queue = Queue(maxsize=300)  #手柄控制器
camera_quee = Queue(maxsize=300)  # 视频流
lcd_quee = Queue(maxsize=300)  # lcd

# 定义ANSI转义序列的颜色代码
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RESET = '\033[0m'


def empty_method(msg=''):
    print(f"{Fore.YELLOW}{msg}=False{Style.RESET_ALL}")


# 创建websocket服务
class WebsocketServices():

    def __init__(self):
        if os.getenv('WEBSOCKET') == "True":
            self.sender_thread = threading.Thread(target=start_websocket,
                                                  args=(queue, ))
        else:
            self.sender_thread = threading.Thread(target=empty_method,
                                                  args=('WEBSOCKET', ))

    def start(self):
        self.sender_thread.start()
        return self

    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


# 创建gamepad服务
class GamepadServices():

    def __init__(self):
        if os.getenv('GAMEPAD') == "True":
            self.sender_thread = threading.Thread(target=gamepad,
                                                  args=(queue, ))
        else:
            self.sender_thread = threading.Thread(target=empty_method,
                                                  args=('GAMEPAD', ))

    def start(self):
        self.sender_thread.start()
        return self

    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


class HttpServer():

    def __init__(self):
        if os.getenv('HTTP') == "True":
            self.sender_thread = threading.Thread(target=http_server,
                                                  args=(camera_quee, ))
        else:
            self.sender_thread = threading.Thread(target=empty_method,
                                                  args=('HTTP', ))

    def start(self):
        self.sender_thread.start()
        return self

    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


class Camera():

    def __init__(self):
        if os.getenv('OPENCV') == "True":
            self.sender_thread = threading.Thread(target=video_stream,
                                                  args=(camera_quee, ))
        else:
            self.sender_thread = threading.Thread(target=empty_method,
                                                  args=('OPENCV', ))

    def start(self):
        self.sender_thread.start()
        return self

    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


class Lcd():

    def __init__(self):
        if os.getenv('LCD') == "True":
            self.sender_thread = threading.Thread(target=lcd_driver,
                                                  args=(lcd_quee, ))
        else:
            self.sender_thread = threading.Thread(target=empty_method,
                                                  args=('LCD', ))

    def start(self):
        self.sender_thread.start()
        return self

    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


def main():
    print("加载模块...")
    web = HttpServer().start()
    ws = WebsocketServices().start()
    vc = Camera().start()
    gpd = GamepadServices().start()
    lcd = Lcd().start()
    # 主线程获取并处理输出结果
    while True:
        try:
            output = queue.get()
            # print("Received:", output)

        except KeyboardInterrupt:
            # 捕捉 Ctrl+C，退出循环
            web.end()
            ws.end()
            vc.end()
            gpd.end()
            lcd.end()
            break


if __name__ == '__main__':
    # 注册信号处理程序，使 Ctrl+C 信号能够被捕获
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
