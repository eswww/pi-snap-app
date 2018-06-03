import io
import asyncio
import socket

host = '127.0.0.1'
port = 2324

loop = asyncio.get_event_loop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(False)
s.bind((host, port))
s.listen(10)

async def handler(conn):
    while True:
        msg = await loop.sock_recv(conn, io.DEFAULT_BUFFER_SIZE)
        print(msg, len(msg))
        if not msg:
            break
    conn.close()

async def server():
    while True:
        conn, addr = await loop.sock_accept(s)
        loop.create_task(handler(conn))

loop.create_task(server())

loop.run_forever()
loop.close()
