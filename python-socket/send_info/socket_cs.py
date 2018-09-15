# coding=utf-8
#!/usr/bin/python

import socket
import commands
import argparse
import traceback
import time
import datetime
import sys

PLATFORM = sys.platform
print("platform is %s" % PLATFORM)

def getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell."""
    import os
    if PLATFORM != "win32":
        cmd = '{ ' + cmd + '; } 2>&1'
    pipe = os.popen(cmd, 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    return sts, text

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# parser.add_argument('host', type=str, help="socket server IP") must be set
# parser.add_argument('--host', type=str, help="socket server IP") can be free

parser = argparse.ArgumentParser(description='this script contains socket server & client')
parser.add_argument('--host', type=str, default = get_host_ip(), help="socket server IP")
parser.add_argument('--port', type=int, default = 5000, help="socket server PORT")
parser.add_argument('role', type=str, help="only 'server' and 'client' are supported")
args = parser.parse_args()

HOST = args.host
PORT = args.port
ROLE = args.role

print("%s:%s %s start" % (HOST, PORT, ROLE))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

if ROLE == "server":
    s.bind((HOST,PORT))
    s.listen(10)         # start TCP listen, only 1 request
    while 1:
        conn,addr = s.accept() 
        print('connected from %s:%s' % addr)
        while 1:
            data = conn.recv(1024)
            if len(data) != 0:
                print("data from client %s:%s len:%s" % (addr, data, len(data)))
            else:
                conn.close()
                break
    print("connection closed by client:%s" % addr)
    
if ROLE == "client":
    s.connect((HOST,PORT))
    while 1:
        # cmd=raw_input("please input cmd:")
        time.sleep(1)
        now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("send time:%s" % now_time)
        s.sendall(now_time)
        # data=s.recv(1024)
        # print(data)
    s.close()

        