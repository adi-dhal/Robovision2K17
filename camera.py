import cv2
import numpy as np
from values import *
from pyimagesearch.shapedetector import ShapeDetector
import time
import math


class Camera:
    targets=[]
    cap = None
    bot=[]
    poss_bot=[]
    def __init__(self):
        frame = None
        while(1):
            self.cap = cv2.VideoCapture(1)
            cap = self.cap
            if cap.isOpened():
                print ("Video Opened")
                break
            else:
                print ("Connection Failed, Trying again: ")
        for i in range(0,10):
            _,frame = cap.read()
        while(1):
            _, frame = cap.read()
            if frame is None:
                print("got no frame")
                continue
            sd = ShapeDetector()
            for color in color_range:
                cnts = self.getcontors(color,frame)
                
                for c in cnts:#marice implementation
                    area = cv2.contourArea(c)
                    print ("Contor %s :: area: %d " %(color,area))
                    M = cv2.moments(c)
                    try:
                            cX = int((M["m10"] / M["m00"]))
                            cY = int((M["m01"] / M["m00"]))
                    except:
                            cX=None
                            cY=None
                    print(cX,cY)

                    sides=sd.detect(c)              #change return value of shape detector
                    value=color_val[color]          #change formula

                    lay=[]
                    cord=(cX,cY)
                    lay.append(cord)
                    lay.append(value)
                    lay.append(sides)

                    if color != bot_color or (sides!=3 and sides!=4) :   #asiign color of bot
                        self.targets.append(lay)
                    else:
                        self.poss_bot.append(lay)

                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv2.imshow("Frame",frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break
        
    def check(self,upd=False):
        for front in self.poss_bot:
            if front[2] == 3:
                for back in self.poss_bot:
                    if back[2] == 4:
                        if(math.sqrt(math.pow((front[0][0]-back[0][0]),2)+math.pow((front[0][1]-back[0][1]),2)) <= bot_dist):#assign value of  distancee between
                            self.bot.append(front)
                            self.bot.append(back)
                            break
        self.poss_bot = []
        if upd == True:
            return
        for con in self.poss_bot:
            if con not in self.bot:
                self.targets.append(con)

    def end(self):
        self.cap.release()
        cv2.destroyAllWindows()
            
    def loc_bot(self,color):
        cap = self.cap
        if not cap.isOpened():
            cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("Cannot connect to video feed")
            return
        _, frame = cap.read()
        if frame is None:
            print("loc_bot_got no frame")
            return
        
        sd = ShapeDetector()
        cnts = self.getcontors(color,frame)
        for c in cnts:
            M = cv2.moments(c)
            try:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
            except:
                    cX=None
                    cY=None
            sides=sd.detect(c)#change return value of shape detector
            value=color_val[bot_color]*sides
            if (sides!=3 and sides!=4):
                continue
            lay=[]
            cord=[cX,cY]
            lay.append(cord)
            lay.append(value)
            lay.append(sides)
            self.poss_bot.append(lay)
            #cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        #cv2.imshow("Frame",frame)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #print(self.poss_bot)
        self.bot = []
        self.check(True)
        if(len(self.bot)!=2):
            print("Bot Not Found %s"%self.bot)
        else:
            return ((self.bot[0][0][0]*0.35 + self.bot[1][0][0]*0.65) , (self.bot[0][0][1]*0.35 + self.bot[1][0][1]*0.65))

    def getcontors(self,color,frame,alow=1000,ahigh=500000):
        result = []
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # define range of color in HSV
        (low,high) = color_range[color]
        low = np.array(low)
        high = np.array(high)

        # Threshold the HSV image to get only color
        mask = cv2.inRange(hsv, low, high)
        mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,(5,5))      ##Changed from 20,20
        cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            area = cv2.contourArea(c)
            if area < ahigh and area >alow:
                result.append(c)
        return result
