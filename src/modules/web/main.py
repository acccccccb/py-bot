# -*- coding: utf-8 -*-
import os
import http.server
import socketserver
import asyncio

def http_server(queue):
    
    # 指定服务器的端口号
    PORT = 8090
    # 指定工作目录路径
    WWWROOT_DIR = os.path.join(os.getcwd(), 'src', 'wwwroot')

    # 将工作目录更改为指定目录
    os.chdir(WWWROOT_DIR)

    # 创建一个静态文件处理器
    handler = http.server.SimpleHTTPRequestHandler

    # 使用指定的端口号启动服务器
    
    
    def main():
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("Server started on port", PORT)
            httpd.serve_forever()
            asyncio.Future()  # run forever

    asyncio.run(main())
