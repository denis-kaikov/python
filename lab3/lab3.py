#!/usr/bin/python3

import argparse
import os
import json
from pathlib import Path
parser = argparse.ArgumentParser()
parser.add_argument("-P", "--pid", action="store_true")
parser.add_argument("-u", "--uid", action="store_true")
parser.add_argument("-g", "--gid", action="store_true")
parser.add_argument("-e", "--env", action="append")

parser.add_argument("-d", "--dir")
parser.add_argument("-p", "--pos",nargs="+", action="append")
parser.add_argument("-f", "--file", type=argparse.FileType("r"))

args = parser.parse_args()
print(args)
data = {}

if args.pid:
    data["pid"]=os.getpid()
if args.uid:
    data["uid"]=os.getuid()
if args.gid:
    data["gid"]=os.getgid()
if args.env:
    data["env"]={}
    for i in args.env:
        data["env"][i]=os.environ[i]
if args.dir:
    path=Path(args.dir)
    os.chdir(path)
    data["dir"]=[]
    for files in path.iterdir():
        if files.is_file():
            data["dir"].append(files.name)
if args.pos:
    data["pos"]=[]
    for i in args.pos:
            for k in i:   data["pos"].append(k)
if args.file:
    s= args.file.readline()
    s =json.loads(s)
    data = dict(s, **data)


data = json.dumps(data, indent = 3)
print(data)
file = open(os.getcwd() + "/data.json", "w+")
file.write(data)
file.close()
