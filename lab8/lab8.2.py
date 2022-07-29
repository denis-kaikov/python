#!/usr/bin/python3

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 10000))
s.listen(2)

dict={}

def handle_sig():
    for i in range(s_num):

        try:
            dsock[i].settimeout(0.001)
            data = dsock[i].recv(1024)
        except socket.timeout:
            continue
        if len(data)==0: del_sock(dsock[i])

        lines = data.decode().splitlines()
        metod, path, _ = lines[0].split()

        lines = lines[1:]
        headers = {}
        body = ""
        header_lines = []
        for k, l in enumerate(lines):
            if len(l) == 0:
                header_lines = lines[:k]
                body = "".join(lines[k+1:])
        for l in header_lines:
            name, value = l.split(":", maxsplit=1)
            headers[name.strip()]=value.strip()

        if metod == "GET":
            if path == "/calculate":
                send_response(dsock[i],405,"Not allowed",i)
                break
            try:
                send_response(dsock[i],200,"ok",i,dict[path])
            except KeyError:
                send_response(dsock[i],404,"Not found",i)
        elif metod == "PUT":
            if path == "/calculate":
                send_response(dsock[i],405,"Not allowed",i)
                break
            dict[path] = body
            send_response(dsock[i],200,"ok",i)
        elif metod == "POST":
            try:
                if  path != "/calculate": send_response(dsock[i],405,"Not allowed",i)
                elif "Operation" in headers:
                    if headers["Operation"]=="+" or  headers["Operation"]=="-" or headers["Operation"]=="*" or headers["Operation"]=="/":
                        value=list(dict.values())
                        repl = value[0]
                        for item in value[1:] :
                            repl=eval(str(repl)+headers["Operation"]+item)
                        send_response(dsock[i],200,"ok",i,str(repl))
                    else: send_response(dsock[i],405,"Not allowed",i)
                else: send_response(dsock[i],200,"ok",i,str(sum({k:int(v) for k,v in dict.items()}.values())))
            except IndexError:
                send_response(dsock[i],404,"Not found",i)

def send_response(cur_sock, code, status, cur_num, body=None):
    rsp = "HTTP/1.1 %d %s \r\n" %(code, status)
    rsp +="Content-lenght = %d\r\n" %(0 if body == None else len(body))
    if body!=None: rsp+=body + "\r\n"

    cur_sock.send(rsp.encode())
    del_sock(cur_sock, cur_num)


dsock=[]
client_addr=[]
global s_num
s_num =0
def del_sock(cur_sock, cur_num):
    cur_sock.close()
    dsock.pop(cur_num)
    client_addr.pop(cur_num)
    global s_num
    s_num-=1
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
            handle_sig()
except KeyboardInterrupt:
    s.close()
