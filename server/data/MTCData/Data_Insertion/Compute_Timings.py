#### compute timings and insert into respective area

import math
from pymongo import MongoClient
client = MongoClient()
db = client.temp5

def get_coordinate_list(stopname):
  bsobj=db.busStop.find({'stopName' : stopname})
  coord=[]
  coord.append(float(bsobj[0]['coord']['lat'].encode('UTF8')))
  coord.append(float(bsobj[0]['coord']['lng'].encode('UTF8')))
  return coord

def compute_distance(bslist):
 
  total_distance=0.0
  double_list=[]
  return_list=[]

  for j in range(0,len(bslist)-1):
    coord1=get_coordinate_list(bslist[j])
    
    double_list.append(coord1)
    coord2=get_coordinate_list(bslist[j+1])
    if(j==len(bslist)-2):
      double_list.append(coord2)
    z=distance(coord1,coord2)
    total_distance=total_distance+z
  return_list.append(total_distance)
  return_list.append(double_list)
  return return_list

def get_minutes(time_str):

  timelist=time_str.split(".")
  hours=int(timelist[0])
  minutes=int(timelist[1])
  final_minutes=(hours*60)+minutes
  return final_minutes


def toRadians(deg):
  return (deg * math.pi) / 180;



def distance(coordA, coordB):
  R = 6371000
  z1 = toRadians(coordA[0]);
  z2 = toRadians(coordB[1]);
  dz = toRadians(coordB[0] - coordA[0]);
  dl = toRadians(coordB[1] - coordA[1]);

  a = ( math.sin(dz/2)*math.sin(dz/2) ) + ( math.cos(z1)*math.cos(z2)*math.sin(dl/2) * math.sin(dl/2))

  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));
  d = R * c;
  d=d/1000.0
 
  return d

bus_data=db.minibus3.find()
MasterBus_data=db.MasterBus.find()
count=0
for bus_document in bus_data:
  count=count+1
  mini_num=bus_document['busNo']
  mini_num=mini_num.encode('UTF8')
  mini_id=bus_document['id']

  mini_src=bus_document['source'].encode('UTF8')
  

  mini_dst=bus_document['destination'].encode('UTF8')
  
  mini_starttime=bus_document['startTime'].encode('UTF8')
  
  starttime_in_minutes=get_minutes(mini_starttime)
  MasterBus_data=db.MasterBus.find({ 'source':mini_src,'destination':mini_dst,'busNo':mini_num })
  bslist=MasterBus_data[0]['busStopList']
  avg_travel_time=MasterBus_data[0]['avgTravelTime']
  total_distance=0
  double_list=[]
  try:
    avg_travel_time=int(avg_travel_time.encode('UTF8'))
    val=compute_distance(bslist)
    total_distance=val[0]
    double_list=val[1]
  except:
    val=compute_distance(bslist)
    total_distance=val[0]
    double_list=val[1]
    speed=10.0
    avg_travel_time=(total_distance/speed)*60
  
  avg_travel_time_hr=avg_travel_time/60.0;

 
  val=compute_distance(bslist)
  total_distance=val[0]
  double_list=val[1]
  
  avg_speed=total_distance/avg_travel_time_hr
  
  shift_list=[]
  shift_list.append(starttime_in_minutes)
  
  current_min=starttime_in_minutes
  for j in range(0,len(bslist)-1):
    coord1=get_coordinate_list(bslist[j])
    coord2=get_coordinate_list(bslist[j+1])
    stop_dist=distance(coord1,coord2)
    shift_time=stop_dist/avg_speed
    shift_time_in_min=int(shift_time*60);
    current_min=current_min+shift_time_in_min

    if(j==len(bslist)-2):
      lost_time=avg_travel_time-(current_min-shift_list[0])
      
      shift_list.append(current_min+lost_time)
    else:
      shift_list.append(current_min)
  
  time_stop_list=[]
  for k in range(len(shift_list)):
    temp0={}
    temp0={
    "busStop" : bslist[k],
    "time" : shift_list[k]
    }
    time_stop_list.append(temp0)

  data0={
  "id" : mini_id,
  "source" : mini_src,
  "destination" : mini_dst,
  "busNo" : mini_num,
  "averageSpeed" : avg_speed,
  "Timings" :time_stop_list

  }
  rid=db.bus.insert_one(data0)  
  