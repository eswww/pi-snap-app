import os
import io

import socket
import asyncio
from multiprocessing import Process, Queue

from gpiozero import Button
from guizero import App, PushButton, Text, Picture

from camera import Camera


def cam_control():
    global cam, q
    cam.new_picture()
    while True:
        data = q.get()
        print('[consumer] ' + str(data))
        if data != '1':
            continue
        cam.take_picture()
        break
    print('[consumer] done')

def server_init():
    print('server init')
    loop.create_task(server_task())
    loop.run_forever()
    loop.close()

async def server_handler(conn):
    global q
    while True:
        msg = await loop.sock_recv(conn, io.DEFAULT_BUFFER_SIZE)
        print(msg, len(msg))
        q.put(msg.decode('utf8'))

        if not msg:
            break
    conn.close()

async def server_task():
    while True:
        conn, addr = await loop.sock_accept(server)
        loop.create_task(server_handler(conn))


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 2324
    q = Queue()

    cam = Camera()

    # Setting server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind((host, port))
    server.listen(10)
    loop = asyncio.get_event_loop()

    proc = Process(target=server_init)
    proc.start()

    app = App('Pi-Snap')
    txt = Text(app, 'Welcome to Pi-Snap!')
    new_pic_icon = PushButton(app, cam_control, text='New pic')
    take_pic_icon = PushButton(app, cam.take_picture, text='take pic')
    app.display()
