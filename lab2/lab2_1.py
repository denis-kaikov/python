#!/usr/bin/python3
import json
import sys
import os
from pathlib import Path
def child_dir(path):
    path = Path(path)
    info = []
    for child in path.iterdir():
        if(child.is_dir()):
            info.append({"type": "dir","name": child.name, "children": child_dir(path / child.name)})
        else:
            info.append({"type": "normal","name": child.name, "size": child.stat().st_size})
    return info

data = {"children":child_dir(sys.argv[1])}
data= json.dumps(data, indent = 3)
print (data)
file=open(os.getcwd()+"/data.json","w+")
file.write(data)
file.close()
