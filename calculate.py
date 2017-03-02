from Client_ble import *
from values import *
from camera import *
import math
import time

def get_route(targets):
    return targets

def mod(vec):
    return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

def dist(v1,v2):
    return math.sqrt((v1[0]-v2[0])*(v1[0]-v2[0]) + (v1[1]-v2[1])*(v1[1]-v2[1]))

def sin(v1,v2):
    #print("sin : ",v1,v2)
    crs = (v1[0]*v2[1] - v1[1]*v2[0])
    m1 = mod(v1)
    m2 = mod(v2)
    return crs/m1/m2

def move_to(dest,cam,mybot):
    fail_count = 0
    msg = ""
    #print("dest:")
    #print(dest,"\n\n")
    while(1):
        bot_loc = cam.loc_bot(bot_color)
        #print("bot_loc")
        #print(bot_loc)
        if bot_loc is None:
            mybot.send_msg('1')
            continue
        v_dest = ((dest[0] - bot_loc[0]),(dest[1] - bot_loc[1]))
        v_bot = ((cam.bot[0][0][0] - cam.bot[1][0][0]), (cam.bot[0][0][1] - cam.bot[1][0][1]))
        #print("\nDestination and bot vectors:\n")
        #print(v_dest)
        #print(v_bot)
        if dist(bot_loc,dest) < 20:#changed from 50 to 20 not less than 20
            print("REACHED Destination")
            mybot.send_msg('6')
            mybot.send_msg('6')
            time.sleep(3)
            return
        angle = sin(v_dest,v_bot)
        #print("angle: ",angle)
        if angle >0:
            if angle < 0.05:
                msg = '1'
            elif angle < 0.4:
                msg = '2'   #"left"
            else:
                msg = '4'   #"sharp_left"
        elif angle < 0:
            if angle > -0.05:
                msg = '1'
            elif angle >  -0.4:
                msg = '3'   #"right"
            else:
                msg = '5'   #"sharp_right"
        else:
            msg = '1'       #"up"

        if True or mybot.checkconnection == True:
            mybot.send_msg(msg)
            print(msg)
        else:
            print("connection_lost")
            fail_count +=1
    
