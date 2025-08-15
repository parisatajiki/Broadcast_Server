import websockets
import asyncio
import aioconsole  # برای ورودی async

async def listen():
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url, ping_interval=None) as ws:
        username = input("Enter your name: ")
        await ws.send(username)

        async def send_messages():
            while True:
                msg = await aioconsole.ainput()
                await ws.send(msg)

        async def receive_messages():
            while True:
                msg = await ws.recv()
                print(msg)

        async def keep_alive():
            while True:
                await asyncio.sleep(30)  # هر ۳۰ ثانیه
                await ws.send("__ping__")  # پیام مخفی پینگ

        await asyncio.gather(send_messages(), receive_messages(), keep_alive())

asyncio.run(listen())
