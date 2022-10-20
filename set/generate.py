#!/usr/bin/python3
# 
# title: 5B Draws of Set
# author: kord.campbell@featurebase.com
# date: 10/19/22

import string
import random

def id(size=4, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# open file
f = open("set_draws.csv", "w")

# create header
f.write("tag__String,time__RecordTime_2006-01-02,thing__String_F_YMD\n")

# create entries
foo = 0
while True:
	foo = foo + 1
	sid = id()
	thing = id(size=1)
	f.write("{sid},2022-10-29,{thing}\n".format(sid=sid, thing=thing))
	if foo > 100000000:
		break

# close file
f.close()