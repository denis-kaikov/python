#!/usr/bin/python3
import evdev
import json
import sys
import os
dev = evdev.InputDevice("/dev/input/event" + sys.argv[1])
data=[]
try:
    for ev in dev.read_loop():
        _ev = evdev.categorize(ev)
        if isinstance(_ev, evdev.KeyEvent):
            event = {"type": "EV_KEY","code": evdev.categorize(ev).keycode, "state": ev.value}
            data.append(event)
            print(event)
        if isinstance(_ev, evdev.RelEvent):
            event = {"type": "EV_REL", "value": ev.value}
            data.append(event)
            print(event)
except KeyboardInterrupt:
    if len(sys.argv) < 3 :
        path = os.getcwd()+"/data.json"
    else:
        path = sys.argv[2]
    file = open(path, "w+")
    data = json.dumps(data, indent = 3)
    file.write(data)
    file.close()
    dev.close()
