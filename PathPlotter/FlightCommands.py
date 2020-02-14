import threading
import connectingtofc
from time import sleep

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
    global kill
    global roll
    global pitch
    global yaw
    global throttle
    global arming
    while not kill:
        message=[roll,pitch,yaw,throttle,1500,arming]
        connectingtofc.commands(message)
        sleep(0.01)
    print("Ending sending thread")
        #add code which complies with messages from flight commands

def setroll(value):
    global roll
    roll = value
def setpitch(value):
    global pitch
    pitch = value
def setyaw(value):
    global yaw
    yaw = value
def setthrottle(value):
    global throttle
    throttle = value
def arm():
    global arming
    arming = 1900
def dissarm():
    global arming
    arming = 1500
def stopsend():
    """function which stops the thread if needed"""
    global kill
    kill = True

if __name__ == "__main__":
    #creating thread instance and starting it
    sendingthread = threading.Thread(target=constantsend)
    sendingthread.start()
    dissarm()
    sleep(2)
    arm()
    sleep(2)
    setthrottle(1500)
    sleep(2)
    setthrottle(885)
    sleep(1)
    dissarm()
    stopsend()
