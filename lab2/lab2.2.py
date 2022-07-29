#!/usr/bin/python3
import evdev
import json
import sys
import os
dev = evdev.InputDevice("/dev/input/event" + sys.argv[1])
#получение номера устройства из командной строки
data=[]
#формирование списка событий для последующей записи в файл
try:
    for ev in dev.read_loop():
        #бесконечный цикл с выходом комбинацией ctrl + C
        _ev = evdev.categorize(ev)
        #тип события
        if isinstance(_ev, evdev.KeyEvent):
            #нажата клавиша
            event = {"type": "EV_KEY","code": evdev.categorize(ev).keycode, "state": ev.value}
            data.append(event)
            print(event)
        if isinstance(_ev, evdev.RelEvent):
            #движение мышкой
            event = {"type": "EV_REL", "value": ev.value}
            data.append(event)
            print(event)
except KeyboardInterrupt:
    #выход с помощью комбинации клавиш

    if len(sys.argv) < 3 :
        #если в строке всего два элемента - название программы и номер устройства,
        #то файл сохраняется в текущую директорию
        path = os.getcwd()+"/data.json"
    else:
        #если в командной строке есть третий элемент (путь к файлу в который надо записать события)
        path = sys.argv[2]

    # Открытие файла на запись     
    file = open(path, "w+")
    data = json.dumps(data, indent = 3)
    file.write(data)
    file.close()
    dev.close()
