#!/usr/bin/python
import json

# Открытие файла и чтение в список
file = open("lab1.json")
data = file.read()
#формирование нового списка
dataNew = []
for d in json.loads(data):
    #проверка является ли элемент списком
    if(isinstance(d,list)):
        for i in range(len(d)):
            if i%2 == 0:
                del d[i]
    #проверка является ли элемент словарём
    elif(isinstance(d,dict)):
            d = {k.upper(): d[k] for k in d}
    #проверка является ли элемент строкой
    elif(isinstance(d ,unicode)):
        d = d[:len(d)/2]
    #записсь преобразованного(или нет) элемента в новый список
    dataNew.append(d)

print (json.dumps(dataNew, indent=4))
