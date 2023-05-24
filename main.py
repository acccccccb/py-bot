# -*- coding: utf-8 -*-

import signal
import subprocess
import threading
from multiprocessing import Process, Queue
from typing import Any
# from src.modules.speak.main import speak
from src.modules.gamepad.main import gamepad
from src.modules.socket.main import start_websocket
from src.modules.web.main import http_server

# 创建队列用于存储输出结果
queue = Queue()

# 创建websocket服务
class WebsocketServices():
    def __init__(self):
        self.sender_thread = threading.Thread(target=start_websocket,args=(queue,))
    def start(self):
        self.sender_thread.start()
        return self
    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join() 

# 创建gamepad服务
class GamepadServices():
    def __init__(self):
        self.sender_thread = threading.Thread(target=gamepad,args=(queue,))
    def start(self):
        self.sender_thread.start()
        return self
    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join() 

class HttpServer():
    def __init__(self):
        self.sender_thread = threading.Thread(target=http_server,args=(queue,))
    def start(self):
        self.sender_thread.start()
        return self
    def end(self):
        if self.server_thread is not None and self.server_thread.is_alive():
            self.server_thread.join()


def main():
    gpd = GamepadServices().start()
    ws = WebsocketServices().start()
    web = HttpServer().start()
    # 主线程获取并处理输出结果
    while True:
        try:
            output = queue.get()
            # print("Received:", output)

        except KeyboardInterrupt:
        # 捕捉 Ctrl+C，退出循环
            web.end()
            ws.end()
            gpd.end()
            break

if __name__ == '__main__':
    # 注册信号处理程序，使 Ctrl+C 信号能够被捕获
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
