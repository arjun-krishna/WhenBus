### this one will insert the info about masterbus ### have to convert to objects


import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient

client = MongoClient()
db = client.temp5

busnolist=[]

busnumfile=open("super_busno.txt","r")


for val in busnumfile:
	num=val.rstrip('\n')
	busnolist.append(num)

for number in busnolist:
	r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode="+number+"&submit=Search")
	soup=BS(r.text,'html.parser')
	table = soup.findAll('table')
	mytable= table[6]
	trows=mytable.findAll('tr')

	reqrow=trows[2].findAll('td')
	busnum=reqrow[0].text
	servicetype=reqrow[1].text
	
	journeytime=reqrow[4].text
	tempstopslist=[]
	uplimit=len(trows)-7
	for j in range(5,5+uplimit):
		tds=trows[j].findAll('td')
		stopnametd=tds[0].findAll('td')
		stopname=stopnametd[0].text
		tempstopslist.append(stopname)
	origin=tempstopslist[0]
	destination=tempstopslist[-1]

	origin=origin.encode('UTF8')
	destination=destination.encode('UTF8')
	servicetype=servicetype.encode('UTF8')
	journeytime=journeytime.encode('UTF8')
	finalbuslist=[]
	finalbuslist=[x.encode('UTF8') for x in tempstopslist]
	
	data={
	"busNo" : number,
	"source" : origin,
	"destination" : destination,
	"serviceType" : servicetype,
	"avgTravelTime" : journeytime,
	"busStopList"  : finalbuslist,
	"buslist" : []
	}
	result=db.masterbus.insert_one(data)