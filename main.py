# MAIN DRIVER FILE

from Client_ble import *
from values import *
from camera import *
from calculate import *
    

##  Initializing variables

#bot = Client()
#Initialize image recognition stuff

##  camera initialize
cam = Camera( )
print("targets:")
print(cam.targets)
print("Possible Bot list:")
print(cam.poss_bot)
cam.check()
targets = cam.targets
print("Bot: \t",cam.bot)
#print("Bot Location: ")
home = cam.loc_bot(bot_color)
#print(home)
print("\n\n")
mybot = Client()
if mybot is None:
    print("CLIENT NOT CONNECTED")
#mybot = None
route = get_route(targets)
loot = 0
for dest in route:
    if loot == 2:
        print("MOVE TO HOME")
        move_to(home,cam,mybot)
        loot = 0
    else:
        print("MOVE TO DEST: ",dest)
        move_to(dest[0],cam,mybot)
        loot += 1

if loot != 0:
    print("RETURN TO HOME")
    move_to(home,cam,mybot)
print("\nPROGRAM COMPLETE\n")
## Hue 0 to 179  0,255, 0 to 255
