#!/usr/bin/python3

import argparse
import os
import json
from pathlib import Path

parser = argparse.ArgumentParser()
# запись всех необходимых элементов

parser.add_argument("-P", "--pid", action="store_true")#PID процесса по ключу "pid". Беззначений.
parser.add_argument("-u", "--uid", action="store_true")#UID пользователя по ключу "uid". Беззначений.
parser.add_argument("-g", "--gid", action="store_true")#GID группы пользователя по ключу "gid". Беззначений.
parser.add_argument("-e", "--env", action="append")    #словарь со значениями указанныхпеременных окружения.
parser.add_argument("-d", "--dir")                     #смена текущего каталога на тот, который указан варгументе
parser.add_argument("-p", "--pos",nargs="+", action="append")#В документ добавляется словарь, содержащий значения указанныхпозиционных аргументов
parser.add_argument("-f", "--file", type=argparse.FileType("r"))#добавляется содержимое указанного файла или содержимое потока ввода

args = parser.parse_args()
print(args)
data = {}

#реализация требуемых функуций
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
    #смена директории
    os.chdir(path)
    data["dir"]=[]
    #формирование словаря с названиями файлов в папке
    for files in path.iterdir():
        if files.is_file():
            data["dir"].append(files.name)
if args.pos:
    data["pos"]=[]
    for i in args.pos:
            for k in i:   data["pos"].append(k)
if args.file:
    s= args.file.readline()
    #чтение строки (в файле или комондной строке)
    s =json.loads(s)
    #обновление текущего словаря в соответствии с считаной строкой
    data = dict(s, **data)

# Открытие файла на запись и вывод в командную строку 
data = json.dumps(data, indent = 3)
print(data)
file = open(os.getcwd() + "/data.json", "w+")
file.write(data)
file.close()
