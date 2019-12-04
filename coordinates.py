#Pulkit_Chauhan
#Importing necessary libraries
import cv2
import numpy as np
import os
import pickle
import time
import datetime

#Making a function for mouse click events
def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(circles)<10000:
            #print(x,y)
            circles.append(tuple([x, y]))
            print(circles)

#Loading the video feed (can also perform on live cctv)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
#cap.set(cv2.CAP_PROP_FPS, 13.09)
cv2.namedWindow("Frame1")
cv2.setMouseCallback("Frame1", mouse_drawing)

#Storing the list of coordinates in circles
circles = []
i=0

while True:
    _, frame1 = cap.read()
    sand="[INFO]:Click on the top left and bottom right anywhere in the screen for making a slot"

    for center_position in circles:
        cv2.circle(frame1, center_position, 5, (0, 0, 255), -1)

        if len(circles)%2==0:
            for i in range(0,len(circles)-1,2):

                cv2.rectangle(frame1,circles[i],circles[i+1],(255,0,0),2)
                #Printing the numbers of stalls
                if True:
                    number=i//2
                    number+=1
                    text="{}".format(number)
                    cv2.putText(frame1,text,tuple(circles[i]),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)
    cv2.putText(frame1,sand,(9,29),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)


    cv2.imshow("Frame1", frame1)
    key = cv2.waitKey(27)

    #storing all the marked corrdinates in file.txt which will be used in other code
    pickle.dump(circles, open('file.txt', 'wb'))

    #if press key is d then all the coordinates stored in circles list will be empty
    if key == 100:
        break
    elif key == ord("d"):
        circles = []
    #if press key is b then, the previous stall will be removed
    elif key==ord("b"):
        circles = circles[:len(circles)-2]
    #if press key is q then the loop will break and display window will break
    elif key == ord("q"):
        break

#releasing video feed
cap.release()
cv2.destroyAllWindows()
