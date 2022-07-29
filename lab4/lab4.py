#!/usr/bin/python3

import os
import sys
import time
import signal
import subprocess
import json

#print(os.getpid())

proc=[] #список процессов
data =[]#формирование списка с инфой о процессах
data.append({"name": sys.argv[1]})

#первый процесс
try:
    # реализация перенаправления потока ввода
    point=sys.argv.index("<")
    proc.append(  subprocess.Popen(sys.argv[1:point], stdin=open(sys.argv[point+1]), text=True, stdout=subprocess.PIPE))
except ValueError:
    try:
        # необходимо получить номер последнего аргумента для процесса( после него будет либо | либо он будет последним аргументом в коммандной строке)
        point=sys.argv.index("|")
        # все аргументы включая последний используются для запуска процесса, то есть не важно их количество
        proc.append( subprocess.Popen(sys.argv[1:point], text=True, stdout=subprocess.PIPE))
    except ValueError:
        proc.append(  subprocess.Popen(sys.argv[1:len(sys.argv)], text=True, stdout=subprocess.PIPE))

#последующие процессы запускаются, если имеются |
#отличается от первого процесса перенаравлением потока ввода в следующий из вывода предыдущего
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

#функция обработчик сигналов
def handler(sig, frame):
    for p in proc:
        p.send_signal(sig)
#сами сигналы и вызов функции
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGINT, handler)



for i in range(len(proc)):
    # ожидание завершиения всех процессов и запись кодов которые они возвращают
    proc[i].wait()
    data[i]["code"] =proc[i].returncode
if data[proc_count]["code"]==0:
    #если последний процесс завершился удачно, то записывается его вывод иначе сообщение о принудительном завершении
    data[proc_count]["output"]= dop_proc[proc_count].stdout.read()
else: data[proc_count]["signal"]= "terminated"

# Открытие файла на запись и вывод в командную строку 
data = json.dumps(data, indent = 3)
file = open(os.getcwd() + "/data.json", "w+")
file.write(data)
file.close()
print(data)
