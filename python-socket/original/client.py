# coding=utf-8
#!/usr/bin/python

import socket
HOST='127.0.0.1'
PORT=5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
s.connect((HOST,PORT))
while 1:
    cmd=raw_input("Please input cmd:")
    s.sendall(cmd)
    data=s.recv(1024)
    print data 
    s.close()
