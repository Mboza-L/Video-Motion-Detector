# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:57:25 2020

@author: lukin
"""

import cv2
import time
import pandas
from datetime import datetime


first_frame = None #the inintial frame to compare new objects with
status_list = [None, None]#list to indicate presence of objects(1) versus empty frames (0)
times=[]#list to store time stamps
df = pandas.DataFrame(columns=["Start","End"])#pandas data frame to store objects

video = cv2.VideoCapture(0)
# the number indicates the video is from a camera camera, else enter video file, i.e movie.mp4

#view the video
while True:
    check, frame = video.read()
    status = 0
    
    #for debugging
    #print(check)#check if the video is running
    #print(frame)#numPy array, 3D, colour array with 3 bands
    
    #converts to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0) #gaussian blur: removes noise and increases accuracy
    
    
    if first_frame is None:
        first_frame = gray
        #stores the first frame in the variable to use as a base for comparison   
        continue#go to the begining of the loop till condition is satisfied, don't go to the rest of the code
    
    delta_frame = cv2.absdiff(first_frame, gray)
    
    #set the threshold value
    #thresh_value = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[0]
    #print(thresh_value)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    #incase still see shadows, bump up the threshold
    #Returns a tuple with 2 values, first value suggests the threshold value to set
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2 )
    (cnts,_)= cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #to create the boundary around a moving object
    frame_size=5000
    for contour in cnts:
        if cv2.contourArea(contour)< frame_size:#incase of inaccurate detection, alter frame size 
            continue
        else:
            
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255,0), 3)
            status = 1
            
    #append times to list when status changes from 0 to 1 or vice versa       
    status_list.append(status)
    if status_list[-1]==1 and status_list[-2] ==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2] ==1:
        times.append(datetime.now())

    
    #display windows with various video settings
    cv2.imshow("Grey Frame", gray)#captures the very first frame in grey scale
    #cv2.imshow("Capturing", frame)#captures the very first frame
    cv2.imshow("Delta Frame", delta_frame)  
    cv2.imshow("Threshold Frame", thresh_frame)    
    cv2.imshow("Colour Frame", frame)#the window that will indicate boundaries around moving objects
    
    key = cv2.waitKey(1)
    #0 means hit any key to exit
    #else, time in miliseconds
    #print(gray)
    #print(delta_frame)#difference btn intensities of the corresponding pixels
    
    #to quit video streaming, press "q"
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
    
    #print (status)
#waits for us to press a key for the video frame to be released
print (status_list)
print(times)

video.release()#release the camera when done
cv2.destroyAllWindows()

#saves data to .csv file
for i in range(0, len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")



