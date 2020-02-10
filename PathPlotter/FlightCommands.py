import connectingtofc
import threading
import time

"""This file sets up the basic direction commands which will be needed to move
   the drone. Creates a thread which constantly sends signals to the Flight
   Controller every 0.01 seconds."""
#lets you manually kill the thread if needed by making true
kill = False
#variables that control the drone
roll = 1500
pitch = 1500
yaw = 1500
throttle = 885
arming = 1500
def constantsend():
    """sends the desired values to the FC every 0.01 secconds"""
    while not kill:
        message=[roll,pitch,yaw,throttle,1500,arm]
        commands(message)
        time.sleep(0.01)
        #add code which complies with messages from flight commands

def roll(value):
    #code that aks thread to change roll
    pass
def pitch(value):
    #code that asks thread to change pitch
    pass
def yaw(value):
    #code that tells thread to changes yaw
    pass
def throttle(value):
    #put code that tells thread to change throttle
    pass
def arm():
    #code that arms
    pass
def stopsend():
    """function which stops the thread if needed"""
    kill = True

if __name__ == "__main__":
    #creating thread instance and starting it
    sendingthread = threading.Thread(target=constantsend())
    sendingthread.start()
    stopsend()
