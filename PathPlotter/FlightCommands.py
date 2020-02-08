import connectingtofc

"""This file sets up the basic direction commands which will be needed to move
   the drone."""
"""Note: tests have to be done to figure out how exatly the flight controller
   responds to the messages so that we can figure out if we need to keep on sending
   it in a loop or for how long we need to do that"""
def throttle(value):
    """arguments given to this function must be from 0-(find)"""
    desire = []
    desire+= [0x05dc]*3
    desire+= value
    commands(desire)
def pitch(value):
    """1500 is the neutral value where the drone is level"""
    desire = []
    desire+= 0x05dc
    desire+= value
    commands(desire)
def roll(value):
    """1500 is the neutral value where the drone is level"""
    commands([value])
def yaw(value):
    """1500 is the neutral value where the drone is level"""
    desire = []
    desire+= [0x05dc]*2
    desire+= value
    commands(desire)
