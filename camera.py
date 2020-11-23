from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
from PID import PID
import cv2
import imutils
import time
l=[]
cap = cv2.VideoCapture(0)
greenLower = (-2, 100, 100)
greenUpper = (18, 255, 255)

def pid_process(p, i, d,error):
    P = PID(p,i,d)
    P.initialize()
    output = P.update(error)
    return output

while(True):
    ret, frame = cap.read()
    (H,W) = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Center of the frame 
    C_x= W//2
    C_y= H//2

    cv2.circle(frame, (C_x,C_y), 5, (0, 0, 255), -1) #Frame center 
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
	# only proceed if at least one contour was found
    if len(cnts) > 0:
	    c = max(cnts, key=cv2.contourArea)
	    ((x, y), radius) = cv2.minEnclosingCircle(c)
	    print("Center" ,int(x) ,int(y))
	    M = cv2.moments(c)
	    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    if radius > 10:
	    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2) #Ball Circle
	    cv2.circle(frame, center, 5, (0, 0, 255), -1) #Ball Center

    #Error
    Error = C_x -x
    print("Error:",Error)
    Output = pid_process(1,0,0,Error)
    l.append(Output)
    print("Output:",Output)
    
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(l)


    

        
