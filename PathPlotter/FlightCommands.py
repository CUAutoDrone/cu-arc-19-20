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
    while not kill:
        message=[roll,pitch,yaw,throttle,1500,arm]
        connectingtofc.commands(message)
        sleep(0.01)
    print("Ending sending thread")
        #add code which complies with messages from flight commands

def roll(value):
    roll = value
def pitch(value):
    pitch = value
def yaw(value):
    yaw = value
def throttle(value):
    throttle = value
def arm():
    arm = 1900
def dissarm():
    arm = 1500
def stopsend():
    """function which stops the thread if needed"""
    kill = True

if __name__ == "__main__":
    #creating thread instance and starting it
    sendingthread = threading.Thread(target=constantsend)
    sendingthread.start()
    dissarm()
    sleep(2)
    arm()
    sleep(2)
    throttle(1500)
    sleep(2)
    throttle(885)
    sleep(1)
    dissarm()
    stopsend()
