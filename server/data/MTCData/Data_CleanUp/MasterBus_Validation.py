### this one will validate the info about masterbus ### have to convert to objects


import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient


def check_presence(name,mainlist):
	for elem in mainlist:
		if(name==elem):	
			return True
	return False

client = MongoClient()
db = client.temp2

mainbuslist=[]
mainbusstoplist=[]
file1=open("busstop_coord.txt","r")
file2=open("final_busno.txt","r")
file3=open("buscoordinates.txt","r")
file4=open("ultimate_busno.txt","w")


for line in file2:
	busnum=line.rstrip('\n')
	mainbuslist.append(busnum)
for line in file1:
	busstop=line.rstrip('\n')
	mainbusstoplist.append(busstop)

r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode=&submit=Search")
soup=BS(r.text,'html.parser')

gc=0
Counter=0
for number in mainbuslist:
	
	r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode="+number+"&submit=Search")
	soup=BS(r.text,'html.parser')
	table = soup.findAll('table')
	
	mytable= table[6]
	trows=mytable.findAll('tr')
	
	reqrow=trows[2].findAll('td')
	busnum=reqrow[0].text
	
	tempstopslist=[]
	uplimit=len(trows)-7
	for j in range(5,5+uplimit):
		tds=trows[j].findAll('td')
		stopnametd=tds[0].findAll('td')
		stopname=stopnametd[0].text
		fbname=stopname.encode('UTF8')
		tempstopslist.append(fbname)
	
	gc=0
	for elem in  tempstopslist:
		
		if(check_presence(elem,mainbusstoplist)):
		
			gc=gc+1
	
	if(len(tempstopslist)==gc):
		print "found a perfect bus"
		Counter=Counter+1
		file4.write(number+'\n')