# -*- coding: utf-8 -*-

import os
import asyncio
import websockets
import datetime


def start_websocket(queue):
    WEBSOCKET_PORT = os.getenv('WEBSOCKET_PORT')
    WEBSOCKET_HOST = os.getenv('WEBSOCKET_HOST')

    async def handle_connection(websocket):
        current_time = datetime.datetime.now()
        try:
            while True:
                output = queue.get()
                await websocket.send(output)
                await asyncio.sleep(1/30)
        except websockets.exceptions.ConnectionClosedOK:
            # 连接关闭时的操作
            connected = False
            print(f" {current_time} < Client disconnected: {websocket.id}")
            return 0

    async def main():
        async with websockets.serve(handle_connection, WEBSOCKET_HOST, WEBSOCKET_PORT):
            print(f"socket running on: {WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
            await asyncio.Future()  # run forever

    asyncio.run(main())

# start_websocket()
