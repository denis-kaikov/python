#!/usr/bin/python3

import redis

r = redis.Redis()

if r.lrange("clist",0,1) == []:

    r.hset("chash", {"eth0" :"100", "eth2":"20", "eth5" : "30", "eth10" :"4"})
    r.rpush("clist", "eth2", "eth5", "eth6")
clist=[item.decode() for item in r.lrange("clist",0,-1)]
chash=dict(zip([key.decode() for key in r.hkeys("chash")],[vals.decode() for vals in r.hvals("chash")]))
slist = list(set(clist) & set(chash.keys()))
shash = {}
for i in chash:
    if slist.count(i)==0:
        shash[i]="0"
    else: shash[i]=str(int(chash[i]) *2)

r.delete("shash")
r.delete("slist")

r.hmset("shash", shash)
r.lpush("slist", *slist)
r.save()
