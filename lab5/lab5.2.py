#!/usr/bin/python3

from scapy.all import *
import time
import os
import json


data={}

def handle_packet(pkts):

    for pocket in pkts:
        try:
            data[hex(pocket[ICMP].id)]["nrequest"]=data[hex(pocket[ICMP].id)]["nrequest"]+1 if pocket[ICMP].type == 8 else data[hex(pocket[ICMP].id)]["nrequest"]
            data[hex(pocket[ICMP].id)]["nresponses"]= data[hex(pocket[ICMP].id)]["nresponses"]+1 if pocket[ICMP].type == 0 else data[hex(pocket[ICMP].id)]["nresponses"]

            if pocket[ICMP].type == 8:
                data[hex(pocket[ICMP].id)]["last_req"] = pocket.time
            else:    data[hex(pocket[ICMP].id)]["rtt"].append(pocket.time-data[hex(pocket[ICMP].id)]["last_req"])
        except KeyError:

            data[hex(pocket[ICMP].id)]= {"id":hex(pocket[ICMP].id),
            "src": pocket[IP].src if pocket[ICMP].type == 8 else pocket[IP].dst,
            "dst": pocket[IP].dst if pocket[ICMP].type == 8 else pocket[IP].src,
            "nrequest": 1 if pocket[ICMP].type == 8 else 0,
            "nresponses": 1 if pocket[ICMP].type == 0 else 0 }
            data[hex(pocket[ICMP].id)]["rtt"] = []
            data[hex(pocket[ICMP].id)]["last_req"] = pocket.time




try:
    while True:
        pkts= sniff(count = 4, filter="icmp")
        if len(pkts)==0:
            print("\n")
            break
        handle_packet(pkts)
except KeyboardInterrupt:
    print("\n")

finally:
    for d in data.values():
        d["max-rtt"]=max(d["rtt"])
        d["min-rtt"]=min(d["rtt"])
        del d["rtt"]
        del d["last_req"]
    data = json.dumps(data, indent=3)
    print(data)
