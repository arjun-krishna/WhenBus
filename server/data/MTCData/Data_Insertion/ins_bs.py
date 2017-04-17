### final bus stop info insertion into database

import json
from pymongo import MongoClient
client = MongoClient()
db = client.temp5

busnumfile=open("super_busno.txt","r")


busnolist=[]


for val in busnumfile:
	num=val.rstrip('\n')
	busnolist.append(num)

for val in busnolist:
	obj=db.masterbus.find({"busNo" :val})
	bnum=obj[0]['busNo']
	src=obj[0]['source']
	dest=obj[0]['destination']
	tlist1=obj[0]['busStopList']
	st=obj[0]['serviceType']
	att=obj[0]['avgTravelTime']
	cur=db.minibus3.find({"source" : src,"destination": dest,"busNo":bnum})
	
	tbuslist1=[]
	for j in range(cur.count()):
		tbuslist1.append(j+1)

	data1={
	"busNo" : bnum,
	"source" : src,
	"destination" : dest,
	"serviceType" : st,
	"avgTravelTime" : att ,
	"busStopList"  : tlist1,
	"buslist" : tbuslist1
	}
	
	db.MasterBus.insert_one(data1)
	cur=db.minibus3.find({"source" : dest,"destination": src,"busNo":bnum})
	
	tbuslist2=[]
	for j in range(cur.count()):
		tbuslist2.append(j+1)
	
	tlist2=list(reversed(tlist1))
	data2={
	"busNo" : bnum,
	"source" : dest,
	"destination" : src,
	"serviceType" : st,
	"avgTravelTime" : att ,
	"busStopList"  : tlist2,
	"buslist" : tbuslist2
	}
	db.MasterBus.insert_one(data2)	
	
	