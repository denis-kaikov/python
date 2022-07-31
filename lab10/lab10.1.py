#!/usr/bin/python3

import redis
from pyroute2 import IPRoute
import pprint as pp

ipr = IPRoute()
idx = ipr.link_lookup(ifname="enp0s3")[0]

r = redis.Redis()

config=dict(zip([key.decode() for key in r.hkeys("neigh-config")],[vals.decode() for vals in r.hvals("neigh-config")]))
