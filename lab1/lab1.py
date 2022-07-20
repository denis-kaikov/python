#!/usr/bin/python
import json

file = open("lab1.json")
data = file.read()
dataNew = []
for d in json.loads(data):
    if(isinstance(d,list)):
        for i in range(len(d)):
            if i%2 == 0:
                del d[i]
    elif(isinstance(d,dict)):
            d = {k.upper(): d[k] for k in d}
    elif(isinstance(d ,unicode)):
        d = d[:len(d)/2]

    dataNew.append(d)

print (json.dumps(dataNew, indent=4))
