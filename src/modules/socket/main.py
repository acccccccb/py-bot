# -*- coding: utf-8 -*-

import asyncio
import websockets
import datetime


def start_websocket(queue):
    PORT = 8765
    HOST = "0.0.0.0"

    async def handle_connection(websocket):
        current_time = datetime.datetime.now()
        try:
            while True:
                output = queue.get()
                await websocket.send(output)
                await asyncio.sleep(0.16)
        except websockets.exceptions.ConnectionClosedOK:
            # 连接关闭时的操作
            connected = False
            print(f" {current_time} < Client disconnected: {websocket.id}")
            return 0

    async def main():
        async with websockets.serve(handle_connection, HOST, PORT):
            print(f"socket running on: {HOST}:{PORT}")
            await asyncio.Future()  # run forever

    asyncio.run(main())

# start_websocket()
