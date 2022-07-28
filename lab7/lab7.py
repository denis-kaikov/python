#!/usr/bin/python3

import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1", 10000))

try:
    while True:
        s.send(b"Enter a command:")
        rsp = s.recv(1024)
        if len(rsp)==0:
            break
        splt= rsp.decode().split(" ")
        start = 0

        while str(splt[start]) == "" :
            start+= 1
        if len(splt[start])>3:
            if splt[start][0:3]=="Quit":
                print("Quitting")
                break
        if str(splt[start][0])=="Q" :
            print("Quitting")
            break
        elif splt[start]=="T":
            s.settimeout(int(splt[start+1]))
            print("Setting timeout to", int(splt[1]) )
        else: print("Response from ('127.0.0.1', 10000): " + rsp.decode(), end ="")
except socket.timeout:
    print("Timeout expired, quitting")
s.close()
