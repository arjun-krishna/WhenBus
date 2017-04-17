### bus stop data insertion ### temporary

from pymongo import MongoClient
client = MongoClient()
db = client.temp5



mydata=db.masterbus.find()
mainlist=[]

maindict={}
myfile=open("ultimate_busstop.txt","r")
for line in myfile:
	name=line.rstrip('\n')
	maindict[name]=[]

count=0

for document in mydata:
	busstoplist=document["busStopList"]
	busnum=document["busNo"]
	
	for bstop in busstoplist:
		maindict[bstop].append(busnum)
	count+=1

newdata={}
for item in  maindict.items():
	newdata={
	"name" : item[0],
	"buslist" :item[1]
	}
	result=db.tempstop.insert_one(newdata)
