#!/usr/bin/python3

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 10000))
s.listen(2)

dict={}

def handle_sig(s_num):
    for i in range(s_num):

        try:
            dsock[i].settimeout(0.001)
            data = dsock[i].recv(1024)
        except socket.timeout:
            continue
        if len(data)==0:
            dsock.pop(i)
            client_addr.pop(i)
            s_num-=1
            break
        data = data.decode().lstrip()
        try:
            if data[0]=="R":
                data = data[1:data.index("\n")].lstrip()
                dsock[i].send((str(dict[data])+"\n").encode())

            elif data[0]=="W":
                data = data[1:].lstrip()
                dict[data[:data.index(" ")]]=data[data.index(" ")+1:data.index("\n")]
        except KeyError:
            dsock[i].send(("there is no such element\n").encode())
    return s_num
dsock=[]
client_addr=[]
s_num=0
try:
    while True:
        s.settimeout(0.001)
        try:

            new_sock, new_client_addr= s.accept()
            dsock.append(new_sock)
            client_addr.append(new_client_addr)
            s_num+=1
        except socket.timeout:
            s_num = s_num

        if s_num !=0:
            s_num = handle_sig(s_num)
except KeyboardInterrupt:
    s.close()
