import socket

MAX_BUFFER = 4096
s = socket.socket()
server = '127.0.0.1'
port   = 5004
s.connect((server,port))
msg = input('-> ')
s.send(msg.encode('utf-8'))
response = s.recv(MAX_BUFFER).decode('utf-8')
print('Received from server {}'.format(response))
