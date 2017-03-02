import bluetooth
import subprocess 
addr="98:D3:31:40:9E:DD"
port = 1
class Client:
    def __init__(self):
        #nearby_devices = bluetooth.discover_devices(duration=4)
        nearby_devices=addr
        for a in nearby_devices:
            if a == addr:
                found = True
##        if found != True:
##            print("Device not found")
##            return
        #print(addr)
        key='1234'
        port = 1
        subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)
        status = subprocess.call("bluetooth-agent " + key + " &",shell=True)
        try:
            self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.s.connect((addr,port))
        except bluetooth.btcommon.BluetoothError as err:
            pass
    def check_connection(self):
        return True
    def send_msg(self,command):
        
        if command =='KILL':
            self.close()
        self.s.send(command)
    def close(self):
        self.s.close()
        
        
    
