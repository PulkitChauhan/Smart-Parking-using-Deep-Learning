
#Pulkit Chauhan
#Importing all the libraries
import subprocess
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import json
import time
import cv2
import webbrowser
import pandas as pd
import time
import datetime
import pickle
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt , os
import urllib.parse
import requests
import http.client
#import geocoder



prototxt='MobileNetSSD_deploy.prototxt.txt'
model='MobileNetSSD_deploy.caffemodel'
new_list_copy=[]
new_list=[]
#For creating mouse click events manually
def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(circles)<1000:
            #print(x,y)
            circles.append(tuple([x, y]))
            print(circles)

#21 classes can be visualize and detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
#Ignoring all 21 classes except "person" class
IGNORE = set(["background", "aeroplane", "bird", "boat",
	"bottle", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"])

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
print("Loading model")
net = cv2.dnn.readNetFromCaffe(prototxt,model)
print("Starting video stream")
vs=cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#change the above three lines:uncomment
#vs.set(cv2.CAP_PROP_FPS, 13.09)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame1", mouse_drawing)

circles = []
time.sleep(2.0)
fps = FPS().start()
counter=0
#Using pickle lib.--open file.txt
circles = pickle.load(open('file.txt', 'rb'))
i=0
j=0
k=[]
p=0
y=0
date=[]
stall_no=[]
no_of_per=[]

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)
'''
mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log'''
#mqttc.username_pw_set("cpfjxexh", "0R1pH_favGt7")
#mqttc.connect('m16.cloudmqtt.com',17887, 60)
#mqttc.loop_start()

#iterating every frame using while loop
while True:

          l=[]
          status,frame = vs.read()
          #img_res = requests.get("http://100.86.155.129:8080/shot.jpg")
          #img_arr = np.array(bytearray(img_res.content), dtype = np.uint8)
          #frame = cv2.imdecode(img_arr,-1)
          #uncomment the status,frame line.
          p=0
          y=0
          #frame = imutils.resize(frame, width=400)
          (h, w) = frame.shape[:2]
          blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                    0.007843, (300, 300), 127.5)

          net.setInput(blob)
          detections = net.forward()
          #print(detections.shape)
          for i in np.arange(0, detections.shape[2]):

                    confidence = detections[0, 0, i, 2]

                    if confidence > 0.15:
                              idx = int(detections[0, 0, i, 1])

                              if CLASSES[idx] in IGNORE:
                                        continue
                              box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                              (startX, startY, endX, endY) = box.astype("int")

                              label = "{}: {:.2f}%".format(CLASSES[idx],
                                        confidence * 100)
                              cv2.rectangle(frame, (startX, startY), (endX, endY),COLORS[idx], 2)
                              #taking centroid of recangle bounding boxes
                              c1=(startX+endX)//2
                              c2=(startY+endY)//2
                              #storing c1 and c2 in a list
                              centroid=[c1,c2]
                              #print(centroid)
                              l.append(centroid)

                              cv2.circle(frame,tuple(centroid),10,(0,255,255),-4)
                              #y = (startY - 15)//2 if (startY - 15)//2 > 15 else (startY + 15)//2
                              cv2.putText(frame,label,tuple(centroid),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
                              box=frame[startY:endY,startX:endX]
          #print(l)
          if len(l)!=0:
              k=[]
              #print(k)
              for p in range(0,len(circles),2):
                  s1=circles[p]
                  s2=circles[p+1]
                  flag=0
                  #print(flag)
                  #print("ff")
                  for b in l:

                      centroid=b
                      #print(flag)
                      #condition
                      if s1[0]<=centroid[0] and s2[0]>=centroid[0] and s1[1]<=centroid[1] and s2[1]>=centroid[1]:

                          flag+=1

                  k.append(flag)
              #print(k)
              #print("Parking list is:"+str(k))
              total_slots=len(k)
              for z,h in enumerate(k):
                  if h==1:
                      k[z]="OCCUPIED"
                  elif h==0:
                      k[z]="EMPTY"
                  else:
                      print("ERROR :(")

              print(k)
              get_indexes = lambda k, xs: [o for (yl, o) in zip(xs, range(len(xs))) if k == yl]
              inc=get_indexes("EMPTY",k)
              new_list_copy=new_list
              new_list=[s+1 for s in inc]
              print(new_list)
              #g = geocoder.ip('me')
              #address="https://www.google.co.in/maps/@"
              #mall=print(""+str(address)+str(g.latlng[0])+str(",")+str(g.latlng[1])+str(",15z"))
              st=str(new_list)
              #data={'Total Slots': 21, 'Available Slots': st}
              '''conn=http.client.HTTPConnection("localhost",8081)
              conn.request("POST","/app/bookslot.php",{'data':'1'})
              response=conn.getresponse()
              print(response.status,response.reason)'''
              #webbrowser.open("http://localhost:8081/app/bookslot.php?data="+str(new_list))  # Go to example.com

              '''
              data={'Total Slots': 21, 'Available Slots': st}
              r = requests.post("http://localhost:8081/app/bookslot.php", json=data)
              print(r.text)
              '''
              #mqttc.publish("TOTAL SLOTS:",total_slots)
              #mqttc.publish("AVAILABLE SLOTS:",st)
              #mqttc.publish("LOCATION:",mall)
              time.sleep(0)

              for u in range(0,len(k)):
                  if k[u]==1:
                      print("Occupied slots is/are:",u+1)
                      if True:
                          mes="Occupied slots are: {}".format(u+1)
                          cv2.putText(frame,mes,(35,120),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),1)
                      continue

          text2="Total Number of Stalls are {}".format(len(k))
          cv2.putText(frame,text2,(9,29),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

          t=datetime.datetime.now().strftime("%x -%X")
          for z in range(0,len(k)):
              stal=z
              stal+=1
              date.append(t)
              stall_no.append(stal)
              #print(z)
              #print(k[z])
              no_of_per.append(k[z])

          for center_position in circles:

              cv2.circle(frame, center_position, 5, (0, 0, 255), -1)
              if len(circles)%2==0:

                  for i in range(0,len(circles)-1,2):
                      cv2.rectangle(frame,circles[i],circles[i+1],(255,0,0),2)
                      if True:
                          number=i//2
                          number+=1

                          text1="Parking {}".format(number)
                          cv2.putText(frame,text1,tuple(circles[i]),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

          cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
          #print(startX))
          #print(no_of_per)
          cv2.imshow("Frame", frame)
          key = cv2.waitKey(1)
          pickle.dump(circles,open('file.txt','wb'))
          if key==ord("q"):
                break

          fps.update()
#raw_data={'Date':date,'Stall(s) Number':stall_no,'Number of person(s)':no_of_per}
df=pd.DataFrame({'Date':date ,'Parking(s) Number':stall_no,'Number of vehicles(s)':no_of_per})
df.to_csv('dataset.csv')
fps.stop()
print("Elapsed time: {:.2f}".format(fps.elapsed()))
print("Approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()

#vs.stop()
#cap.release()
