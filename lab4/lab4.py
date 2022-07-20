#!/usr/bin/python3

import os
import sys
import time
import signal
import subprocess
import json

#print(os.getpid())

proc=[]
data =[]
data.append({"name": sys.argv[1]})

try:
    point=sys.argv.index("<")
    proc.append(  subprocess.Popen(sys.argv[1:point], stdin=open(sys.argv[point+1]), text=True, stdout=subprocess.PIPE))
except ValueError:
    try:
        point=sys.argv.index("|")
        proc.append( subprocess.Popen(sys.argv[1:point], text=True, stdout=subprocess.PIPE))
    except ValueError:
        proc.append(  subprocess.Popen(sys.argv[1:len(sys.argv)], text=True, stdout=subprocess.PIPE))


proc_count= sys.argv.count("|")
if proc_count!=0:
    for proc_num in range(1,proc_count+1):
        begin = sys.argv.index("|")+1
        data.append({"name": sys.argv[begin]})
        sys.argv[sys.argv.index("|")]=0
        try:
            point=sys.argv.index("|")
            proc.append( subprocess.Popen(sys.argv[begin:point], stdin=proc[proc_num-1].stdout, text=True, stdout=subprocess.PIPE))
        except ValueError:
            proc.append(  subprocess.Popen(sys.argv[begin:len(sys.argv)], stdin=proc[proc_num-1].stdout, text=True, stdout=subprocess.PIPE))


def handler(sig, frame):
    for p in proc:
        p.send_signal(sig)
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGINT, handler)



for i in range(len(proc)):
    proc[i].wait()
    data[i]["code"] =proc[i].returncode
if data[proc_count]["code"]==0:
    data[proc_count]["output"]= dop_proc[proc_count].stdout.read()
else: data[proc_count]["signal"]= "terminated"
data = json.dumps(data, indent = 3)
file = open(os.getcwd() + "/data.json", "w+")
file.write(data)
file.close()
print(data)
