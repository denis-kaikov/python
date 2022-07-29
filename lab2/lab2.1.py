#!/usr/bin/python3
import json
import sys
import os
from pathlib import Path

def child_dir(path):
    #функция-реккурсия: вызывает себя если натыкается на папку
    path = Path(path)
    info = []
    #формирование списка инфы о поддереве
    for child in path.iterdir():
        # Проверка является ли объект директорией, если является, то записывается
        #необходимая информация в список и вызывается функция, в путь добавляется имя папки
        if(child.is_dir()):
            info.append({"type": "dir","name": child.name, "children": child_dir(path / child.name)})
        #Во всех других случаях инфа записывается как о нормальном файле
        else:
            info.append({"type": "normal","name": child.name, "size": child.stat().st_size})
    return info


data = {"children":child_dir(sys.argv[1])}
data= json.dumps(data, indent = 3)
print (data)
# Открытие файла на запись в текущую директорию
file=open(os.getcwd()+"/data.json","w+")
file.write(data)
file.close()
