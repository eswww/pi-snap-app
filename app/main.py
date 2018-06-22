import os
import io

import socket
import asyncio

import threading
from multiprocessing import Process, Queue

from app import Application


def queue_clear():
    global q
    
    while not q.empty():
        q.get()

def cam_control():
    global q

    app.new_picture()
    queue_clear()    # Ignore accumulated data

    while True:
        data = q.get()
        if data != '1':
            continue
        break
    path = app.take_picture()
    app.go_to_result(path)

def button_control():
    global button

    while True:
        if not os.read(button, 0):
            cam_control()

def server_init():
    loop.create_task(server_task())
    loop.run_forever()
    loop.close()

async def server_handler(conn):
    global SIZE, q

    while True:
        msg = await loop.sock_recv(conn, io.DEFAULT_BUFFER_SIZE)

        # Checking queue overflow
        if(q.qsize() == SIZE - 1):
            queue_clear()
        q.put(msg.decode('utf8'))

        if not msg:
            break

    conn.close()

async def server_task():
    while True:
        conn, addr = await loop.sock_accept(server)
        loop.create_task(server_handler(conn))


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 2324
    SIZE = 30    # Maximum queue size

    q = Queue(maxsize=SIZE)
    button = os.open('/dev/button_driver', os.O_RDWR)

    # Setting server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind((HOST, PORT))
    server.listen(10)
    loop = asyncio.get_event_loop()

    # Running server process
    proc = Process(target=server_init)
    proc.start()

    # Running GUI application
    app = Application(cam_control)

    th= threading.Thread(target=button_control)
    th.start()

    app.display()

    # When the application is terminated, Server process is terminated
    proc.terminate()

    os.close(button)
