import json
from pymongo import MongoClient

client = MongoClient()
db = client.temp5                ## Data base i.e used

myfile1=open("ultimate_busstop.txt","r")       ## Final Scrapped busstop list
myfile2=open("lat.txt","r")              ## latitudes uinfo file
myfile3=open("long.txt","r")               ## longitudes info file

latlist=[]
lonlist=[]
bsnamelist=[]

for line in myfile2:
	lat=line.rstrip('\n')
	latlist.append(lat)
for line in myfile3:
	lon=line.rstrip('\n')
	lonlist.append(lon)
for line in myfile1:
	name=line.rstrip('\n')
	bsnamelist.append(name)

for val in range(0,485):
	
	temp={}
	temp['lat']=latlist[val]
	temp['lng']=lonlist[val]

	mybuslist=db.tempstop.find({"name" :bsnamelist[val]})  ## list of all bus numbers that pass through a busstop
	
	data={
	"stopName" : bsnamelist[val],
	"coord" : temp,
	"busList" : mybuslist[0]['buslist']
	}
	result=db.busStop.insert_one(data)  ## data insertion
