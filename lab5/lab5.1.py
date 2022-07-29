#!/usr/bin/python3

from scapy.all import *
import time
import os
import json

data={}
def handle_packet(pkts):
    for pocket in pkts:
        try:
            data[pocket[IP].src]= {"mac":pocket[Ether].src, "age": pocket.time}
            data[pocket[IP].dst]= {"mac":pocket[Ether].dst, "age": pocket.time}
        except IndexError:
            continue


try:
    while True:
        pkts= sniff(count = 2)
        if len(pkts)==0:
            print("\n")
            break
        handle_packet(pkts)
except KeyboardInterrupt:
    print("\n")

finally:
    for d in data.values():

        if time.time()-d["age"]>5:
            del d
        else: d["age"]=time.time()-d["age"]
    data = json.dumps(data, indent=3)
    print(data)
