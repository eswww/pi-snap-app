from guizero import App, PushButton, Text, Picture
from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime
from socket import *
from select import select
import sys


# 호스트, 포트와 버퍼 사이즈를 지정
HOST = '127.0.0.1'
PORT = 2325
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체를 만들고
clientSocket = socket(AF_INET, SOCK_STREAM)

# 서버와의 연결을 시도
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('서버(%s:%s)에 연결 할 수 없습니다.' % ADDR)
    sys.exit()
print('서버(%s:%s)에 연결 되었습니다.' % ADDR)

def take_picture():
    print('take a picture')
    camera.capture(output)
    camera.stop_preview()

def new_picture():
    camera.start_preview()


camera = PiCamera()
camera.resolution = (400, 400)
camera.hflip = True

while True:
    try:
        connection_list = [sys.stdin, clientSocket]

        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            if sock == clientSocket:
                data = sock.recv(BUFSIZE)
                if not data:
                    print('서버(%s:%s)와의 연결이 끊어졌습니다.' % ADDR)
                    clientSocket.close()
                    sys.exit()
                else:
                    print('%s' % data)  # 메세지 시간은 서버 시간을 따른다
                    new_picture
                    prompt()
            else:
                message = sys.stdin.readline()
                clientSocket.send(message)
                prompt()
    except KeyboardInterrupt:
        clientSocket.close()
        sys.exit()