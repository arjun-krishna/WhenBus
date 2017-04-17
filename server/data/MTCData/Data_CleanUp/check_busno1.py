import requests
from bs4 import BeautifulSoup as BS

r=requests.get("http://mtcbus.org/BusTimeSchedule.asp")
soup=BS(r.text,'html.parser')  ## gets bus times html document
busnolist_t=[]
data=[]
myfile1=open("busno_t.txt","w")
myoptions=soup.find("select", {"name": "cboRNO"})  ## get all bus numbers
for option in  myoptions.findAll('option'):
	busnolist_t.append(option.text)

data=[x.encode('UTF8') for x in busnolist_t]
data.sort()
for x in data:
	myfile1.write(x+'\n')

myfile1.close()
