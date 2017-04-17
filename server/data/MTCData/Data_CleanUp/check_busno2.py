import requests
from bs4 import BeautifulSoup as BS

f=open('busno_s.txt','w')   
busnolist_s=[]
r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode=&submit=Search")
soup=BS(r.text,'html.parser')   ## busnumbers in bus routes portal

myoptions=soup.find("select", {"name": "cboRouteCode"})
for option in  myoptions.findAll('option'):
	busnolist_s.append(option.text)

data=[]
data=[x.encode('UTF8') for x in busnolist_s]
data.sort()

for x in data:
	f.write(x+'\n')
f.close()

