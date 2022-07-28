#!/usr/bin/python3

from scapy.all import *

import os
import json
import random

ether = Ether(src="2c:f0:5d:d8:3e:fc", dst="04:bf:6d:07:35:dc")
ip = IP(src="192.168.1.39", dst="195.144.107.198")
sport=random.randint(10000, 20000)
next_seq=0
next_ack=0
tcp = TCP(seq=next_seq, ack=next_ack, flags="S",sport=sport, dport=21)
p = ether/ip/tcp
pkts=srp(p)

rsp=pkts[0][0][1]
#print(repr(rsp))
next_seq+=1
next_ack=rsp[TCP].seq+1

tcp = TCP(seq=next_seq, ack=next_ack, flags="A", sport=sport, dport=21)

p = ether/ip/tcp
pkts=srp(p)
rsp=pkts[0][0][1]
#print(repr(rsp))

next_seq+=1
next_ack=rsp[TCP].seq+1

tcp = TCP(seq=next_seq, ack=next_ack, flags="F", sport=sport, dport=21)

p = ether/ip/tcp
pkts=sendp(p)
print("Server system info: " + rsp[TCP].load.decode())
#raw = Raw("PWD\r\n")

#next_ack=rsp[TCP].seq+len(rsp[TCP].payload)

#tcp = TCP(seq=next_seq, ack=next_ack, flags="A", sport=sport, dport=21)
#p=ether/ip/tcp/raw
#pkts = srp(p)
#print(pkts[0][0][1].load.decode())
