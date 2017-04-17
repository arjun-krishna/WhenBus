import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup as BS
from pymongo import MongoClient



client = MongoClient()
db = client.temp5       ## database that we are using

r=requests.get("http://mtcbus.org/Routes.asp?cboRouteCode=&submit=Search")
soup=BS(r.text,'html.parser')          

browser= webdriver.Chrome(executable_path="/home/vinay/Downloads/chromedriver")
browser.get("http://mtcbus.org/BusTimeSchedule.asp")
time.sleep(1)

busnumfile=open("super_busno.txt","r")           ## final busnumber list
minifile=open("minibusinfo.txt","w")             

mynewbusnolist=[]

for val in busnumfile:
	num=val.rstrip('\n')
	mynewbusnolist.append(num)


selectbusnum= Select(browser.find_element_by_name('cboRNO'))  ## selects the busnumber field in browser
counter=0
suc_counter=0
for p in range(25,len(mynewbusnolist)):
		
		a=db.masterbus.find({"busNo" :mynewbusnolist[p]})
		points=[]

		for document in a:
			stoplist=document['busStopList']
			points.append(document['source'])
			points.append(document['destination'])             ## gets the src and dest from database

		selectbusnum= Select(browser.find_element_by_name('cboRNO')) 
		selectbusnum.select_by_visible_text(mynewbusnolist[p])
		k=0

		for j in range(0,2):	
			z=0
			elem0 = browser.find_element_by_xpath("//*")
			source_code0 = elem0.get_attribute("outerHTML")  ## gets the html document
			soup=BS(source_code0,'html.parser')
			
			selectstop = Select(browser.find_element_by_name('cboFR'))
			selectstop.select_by_visible_text(points[j])
			searchbutton=browser.find_element_by_xpath("//input[@type='submit']")
			searchbutton.click()
			elem = browser.find_element_by_xpath("//*")
			source_code = elem.get_attribute("outerHTML")
			soup=BS(source_code,'html.parser')
			tables=soup.findAll('table')  ## gets all tables 

			if(j==0):
				src=points[0]
				dest=points[1]
			if(j==1):
				src=points[1]
				dest=points[0] 

			num_tables=(len(tables)-6)/2
			pval=-1	
			for k in range(0,num_tables):
				tnum=6+(k*2)
				main_rows=tables[tnum].findAll('tr')
				main_tds=main_rows[0].findAll('td')
				z1=main_tds[1].text
				z2=main_tds[3].text
				if((src in z1) and (dest in z2)):
					suc_counter=suc_counter+1
					pval=k
					break
			if(pval==-1):
				continue
			mynum=6+(pval*2)
			trs=tables[mynum+1].findAll('tr')
			timelist=[]
			gs=0
			for row in trs:
				tds=row.findAll('td')
				for td in tds:
					gs=gs+1
					finaldata={}
					finaldata['id']=gs
					finaldata['busNo']=mynewbusnolist[p]
					finaldata['source']=src
					finaldata['destination']=dest
					finaldata['averageSpeed']=30
					finaldata['startTime']=td.text
					finaldata['Timings']=[]
					timelist.append(td.text)
					finaldata_md={
					"id" : gs,
					"busNo" : mynewbusnolist[p],
					"source" : src,
					"destination" : dest,
					"averageSpeed" : 30,
					"startTime" : td.text,
					"Timings" : []


					}
					result=db.minibus1.insert_one(finaldata_md)
					json.dump(finaldata,minifile)
					minifile.write('\n')

	