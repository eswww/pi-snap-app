import time
import socket

ip = '127.0.0.1'
port = 2324

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.connect((ip, port))

time.sleep(2)
sock.send('0'.encode('utf8'))
time.sleep(2)
sock.send('0'.encode('utf8'))
time.sleep(2)

# Takc Picture !
sock.send('1'.encode('utf8'))
time.sleep(2)

sock.close()
