### does data validation based on the input files

import requests
from bs4 import BeautifulSoup as BS
from pymongo import MongoClient

myfile1=open("busno_s.txt","r")
myfile2=open("busno_t.txt","r")

myfile3=open("temp1.txt","w")
myfile4=open("temp2.txt","w")
myfile5=open("common_temp.txt","w")

list_s=[]
list_t=[]
list2=[]
for line in myfile1:
	val=line.rstrip('\n')
	list_s.append(val)

for line in myfile2:
	val=line.rstrip('\n')
	list_t.append(val)

v=(set(list_s) & set(list_t))

final=[]

for elem in v:
	final.append(elem)
final.sort()

for elem in final:
	list_t.remove(elem)
	list_s.remove(elem)

for elem in list_s:
	myfile3.write(elem+'\n')
for elem in list_t:
	myfile4.write(elem+'\n')
for elem in final:
	myfile5.write(elem+'\n')
myfile3.close()
myfile4.close()


