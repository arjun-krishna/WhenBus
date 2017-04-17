#### gets unique bus stops 
import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient


busnolist=[]

global_stop_list=[]
file1=open("final_busno.txt","r")
for line in file1:
	val=line.rstrip('\n')
	busnolist.append(val)

count=0
finaldict={}
z=0;
for number in busnolist:
	
	r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode="+number+"&submit=Search")
	soup=BS(r.text,'html.parser')
	table = soup.findAll('table')
	
	mytable= table[6]
	trows=mytable.findAll('tr')
	
	reqrow=trows[2].findAll('td')
	tempstopslist=[]
	uplimit=len(trows)-7
	for j in range(5,5+uplimit):
		tds=trows[j].findAll('td')
		stopnametd=tds[0].findAll('td')
		stopname=stopnametd[0].text
		name=stopname.encode('UTF8')
		
		z=z+1
		
		finaldict[name]=1


newlist=[x[0] for x in finaldict.items()]

f1=open("final_busstops.txt","w")

for val in newlist:
	f1.write(val+'\n')
f1.close()

