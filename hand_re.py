import numpy as np
import cv2 as cv
import math
import pyttsx3
import os 
import time

cap = cv.VideoCapture(0)

sign = ['Hello', 'I love you', 'best of luck', 'thank you']



while True:
    lap = 0
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    k = np.ones((3,3), np.uint8)
    region = frame[100:300, 100:300]

    cv.rectangle(frame, (100, 100), (300, 300), (0,255,0), 0)
    hsv = cv.cvtColor(region, cv.COLOR_BGR2HSV)

    lower_skin = np.array([0, 15, 0], dtype=np.uint8)
    upper_skin = np.array([50, 220, 255], dtype=np.uint8)

    mask = cv.inRange(hsv, lower_skin, upper_skin)
    mask = cv.dilate(mask, k, iterations=4)
    mask = cv.GaussianBlur(mask, (5,5), 100)
    contours, hi = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    try:
        cnt = max(contours, key = lambda x: cv.contourArea(x))

    except:
        print("err1")

    epsilon = 0.0005*cv.arcLength(cnt, True)
    approax = cv.approxPolyDP(cnt, epsilon, True)

    hull = cv.convexHull(cnt)

    areahull = cv.contourArea(hull)
    areacnt = cv.contourArea(cnt)

    arearatio = ((areahull-areacnt)/areacnt)*100

    hull = cv.convexHull(approax, returnPoints=False)
    defects = cv.convexityDefects(approax, hull)

    l = 0

    try:
        print("{}, {}".format(arearatio, l))
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i, 0]
            start = tuple(approax[s][0])
            end = tuple(approax[e][0])
            far = tuple(approax[f][0])
            pt = (100, 180)

            a1 = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b1 = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c1 = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            s = (a1+b1+c1)/2
            ar = math.sqrt(s*(s-a1)*(s-b1)*(s-c1))

            d1 = (2*ar)/a1

            angle = math.acos((b1**2 + c1**2 - a1**2)/(2*b1*c1)) * 57

            if(angle <= 90 and d1 > 30):
                l += 1
                cv.circle(region, far, 3, [255, 0, 0], -1)
                cv.line(region, start, end, [0, 255, 0], 2)
    except:
        print("err2")

    l+=1


    font = cv.FONT_HERSHEY_SIMPLEX
    
    abc = 0

    if l==1:
            if areacnt<2000:
                cv.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
            else:
                if arearatio>=6:
                    cv.putText(frame,sign[3],(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

                else:
                    cv.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    elif l==2:
        if(arearatio >= 16):
            cv.putText(frame,sign[0],(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)
  
            #os.system("espeak {}".format(sign[0]))
        else:
            pass
            #cv.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    elif l==3:

          if arearatio<27:
                cv.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

          if arearatio > 50:
                cv.putText(frame,'I Love YOU',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

          else:
                cv.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    elif l==4:
        cv.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    elif l==5:
        cv.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    elif l==6:
        cv.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv.LINE_AA)

    else :
        cv.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv.LINE_AA)


    cv.imshow("frame", frame)
    cv.imshow("hsv", hsv)
    cv.imshow("mask", mask)

    if(cv.waitKey(20) & 0xFF == ord('q')):
        break

cap.release()
cv.destroyAllWindows()
