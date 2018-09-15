# coding=utf-8
#!/usr/bin/python
import socket
import commands
HOST='127.0.0.1'
PORT=5000
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)         # start TCP listen, only 1 request
while 1:
    conn,addr=s.accept() 
    print'Connected by',addr
    while 1:
        data=conn.recv(1024) 
        #commands.getstatusoutput interpretion: run shell command, with two rets, status&result, if status is 0, means success
        cmd_status,cmd_result=commands.getstatusoutput(data)
        # if len of result is 0, means over, like mkdir or create a file, if success, no result will be output
        if len(cmd_result.strip()) ==0:
            conn.sendall('Done.')
        else:
            conn.sendall(cmd_result)   # if failed, return the result
            conn.close()
