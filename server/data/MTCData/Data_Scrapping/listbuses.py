## gets first round of busstops 

import requests
from bs4 import BeautifulSoup as BS

busstoplist=[]
f=open("busstop.txt" ,"r")
for line in f:
	busstoplist.append(line.rstrip('\n'))

for bustsop2 in busstoplist:
	r=requests.get("http://mtcbus.org/Places.asp?cboSourceStageName=ADYAR+B.S.&submit=Search.&cboDestStageName="+bustsop2)
	soup=BS(r.text,'html.parser')
	table = soup.findAll('table')
	trows=table[5].findAll('tr')
	if(len(trows)<=2):
		continue
	else:
		for i in range(1,len(trows)-1):
			tds=trows[i].findAll('td')
			myvalue=tds[1].text
			print myvalue