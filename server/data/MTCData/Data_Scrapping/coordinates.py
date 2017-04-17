### scrapes all the coordinates from mymetrocommute.in website

import time
import requests
from selenium import webdriver
import json
import ast
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup as BS
from pymongo import MongoClient




browser= webdriver.Chrome(executable_path="/home/vinay/Downloads/chromedriver")
data0=browser.get("http://my.metrocommute.in/")
time.sleep(1)

myfile=open("final_busstops.txt","r")
myoutput=open("buscoordinates.txt","w")
count=0
z=0
for line in myfile:
	
	bsname=line.rstrip('\n')
	finalname=bsname.title()


	try:
		mydict={}
		a=browser.get("http://my.metrocommute.in//GetStageInfo?stageName="+finalname)
		body=browser.find_element_by_tag_name("body")
		d = ast.literal_eval(body.text)
		
		if(len(d.items())!=0):
			templist=[]
			templist=d['loc']
			mydict["name"]=bsname
			mydict["loc"]=templist
			json.dump(mydict,myoutput)
			
			myoutput.write('\n')
			count=count+1
	except:
		continue