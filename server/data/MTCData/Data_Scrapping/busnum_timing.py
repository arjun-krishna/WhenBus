import time
import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient
r=requests.get("http://mtcbus.org/BusTimeSchedule.asp")
soup=BS(r.text,'html.parser')
mynewbusnolist=[]

myfile=open("newbusno_timings","w")

### gets bus nums in bus timings list
myoptions=soup.find("select", {"name": "cboRNO"})
for option in  myoptions.findAll('option'):
	mynewbusnolist.append(option.text)
	myfile.write(option.text+'\n')
print mynewbusnolist