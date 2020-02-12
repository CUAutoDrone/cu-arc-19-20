import connectingtofc
import threading
import time
"""this library allows you to send messages between threads. We are trying to
   avoid the threads looking at the same variable in in memory so this miight be
   a solution"""
from queue import Queue

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
messanger = Queue()

def constantsend():
    """sends the desired values to the FC every 0.01 secconds"""
    while not kill:
        "reads desired values to send"
        recieved = messanger.get()
        for i in recieved:
            if i == 'roll':
                roll = i[1]
            elif i == 'pitch':
                pitch = i[1]
            elif i == 'yaw':
                yaw = i[1]
            elif i == 'throttle':
                throttle = i[1]
            elif i == 'arm':
                arm = 1900
            else:
                arm = 1500
        message=[roll,pitch,yaw,throttle,1500,arm]
        commands(message)
        time.sleep(0.01)
    print("Ending sending thread")
        #add code which complies with messages from flight commands

def roll(value):
    messanger.put(['roll',value])
def pitch(value):
    messanger.put(['pitch',value])
def yaw(value):
    messanger.put(['yaw',value])
def throttle(value):
    messanger.put(['throttle',value])
def arm():
    messanger.put(['arm'])
def dissarm():
    messanger.put(["dissarm"])
def stopsend():
    """function which stops the thread if needed"""
    kill = True

if __name__ == "__main__":
    #creating thread instance and starting it
    sendingthread = threading.Thread(target=constantsend())
    sendingthread.start()
    stopsend()
