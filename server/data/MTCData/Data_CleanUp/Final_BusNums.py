## Finalised data based on the scrapped data of bus nums

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup as BS
from pymongo import MongoClient



client = MongoClient()
db = client.temp4

r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode=&submit=Search")
soup=BS(r.text,'html.parser')

browser= webdriver.Chrome(executable_path="/home/vinay/Downloads/chromedriver")
browser.get("http://mtcbus.org/BusTimeSchedule.asp")
time.sleep(1)

busnumfile=open("ultimate_busno.txt","r")
mynewbusnolist=[]


tfile=open("super_busno.txt","w")
for val in busnumfile:
	num=val.rstrip('\n')
	mynewbusnolist.append(num)



selectbusnum= Select(browser.find_element_by_name('cboRNO'))
counter=0
for option in mynewbusnolist:
		a=db.masterbus.find({"busNo" :option})
		points=[]
		for document in a:
			stoplist=document['busStopList']
			points.append(document['source'])
			points.append(document['destination'])
		selectbusnum= Select(browser.find_element_by_name('cboRNO'))
		selectbusnum.select_by_visible_text(option)
		z=0
		elem0 = browser.find_element_by_xpath("//*")
		source_code0 = elem0.get_attribute("outerHTML")
		soup=BS(source_code0,'html.parser')
		myoptions=soup.find("select", {"name": "cboFR"})
		for op in  myoptions.findAll('option'):
			if((op.text==points[0]) or (op.text==points[1])):
				z=z+1
		if(z==2):
			counter=counter+1
			tfile.write(option+'\n')
		else:
			continue
	