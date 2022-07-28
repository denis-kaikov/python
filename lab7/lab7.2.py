#!/usr/bin/python3

import socket
import time
import sys
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("195.144.107.198", 21))

def get_mes():
    rsp=s.recv(1024)
    if int(rsp.decode()[:3])==220 or int(rsp.decode()[:3])==226:
        message= "Autonomous message code, "
    else: message="Reply code, "
    message+= rsp.decode()[:3] + ", text: " + "\'" + rsp.decode()[4:len(rsp)-2] + "\'"
    print(message)
    return (rsp)
def send_ack(text):
    if text.decode()[:4]=="USER":
        text += (sys.argv[1]+ "\r\n").encode()
    elif text.decode()[:4]=="PASS":
        text += (sys.argv[2]+"\r\n").encode()
    elif text.decode()[:4]=="RETR":
        text += (sys.argv[3]+"\r\n").encode()
    print("Sending command:" + repr(text))
    s.send(text)
    return get_mes()



get_mes()
send_ack(b'USER ')
send_ack(b'PASS ')
code = send_ack(b'PASV\r\n').decode()
splt=code.split(",")
port = int(splt[len(splt)-2]) << 8 | int(splt[len(splt)-1][:splt[len(splt)-1].index(")")])
send_ack(b'RETR ')

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(("195.144.107.198", port))


file = open(os.getcwd() + "/file" + sys.argv[3][len(sys.argv[3])-4:],"wb")
while True:
    rsp=s2.recv(1024)
    if len(rsp)==0:
        break
    file.write(rsp)
file.close()
s2.close()

get_mes()
send_ack(b'QUIT\r\n')
s.close()
