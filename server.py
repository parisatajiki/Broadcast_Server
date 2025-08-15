import asyncio
import websockets

PORT = 7890
print(f"Server listening on Port {PORT}")

connected = {}  # {websocket: username}

async def echo(websocket):
    try:
        username = await websocket.recv()
        connected[websocket] = username
        print(f"{username} joined the server")

        for conn in connected:
            if conn != websocket:
                await conn.send(f"🔔 {username} joined the chat")

        async for message in websocket:
            if message != "__ping__":
                print(f"{username}: {message}")
                for conn in connected:
                    if conn != websocket:
                        await conn.send(f"{username}: {message}")

    except websockets.exceptions.ConnectionClosed:
        username = connected.get(websocket, "Unknown")
        print(f"{username} disconnected")
        for conn in connected:
            if conn != websocket:
                await conn.send(f"❌ {username} left the chat")
    finally:
        connected.pop(websocket, None)

async def main():
    # غیرفعال کردن پینگ پیش‌فرض
    async with websockets.serve(echo, "localhost", PORT, ping_interval=None):
        await asyncio.Future()

asyncio.run(main())
