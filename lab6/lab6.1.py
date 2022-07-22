#!/usr/bin/python3

from scapy.all import *
import time
import os
import json


ether = Ether(src="2c:f0:5d:d8:3e:fc", dst="04:bf:6d:07:35:dc")
ip = IP(src="192.168.1.39", dst="24.214.177.39")
udp = UDP(dport=17, sport = 11000)

p=ether/ip/udp
pkts=srp(p)
print(pkts[0][0][1].load.decode())
