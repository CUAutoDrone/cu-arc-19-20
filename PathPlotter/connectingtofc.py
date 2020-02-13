import serial
from time import sleep
import struct

def connecttoport(dport):
    """This function connect to the desired port"""
    port= serial.Serial(dport,115200, timeout=10, write_timeout=10)
    print("Desired port is "+port.name)
    return port


def send(dmsg, port):
    """This function is what is used to send the final message. It takes the port
    you want and the message as arguments."""
    port.write(dmsg)


def pack(channels):
    """This function packs the desired message in the ibus format. You give it the
    values for all 14 channel in an array. Unused channels must be given the
    value 0x05DC"""
    message=[]
    #adds the required begining header of the message
    message.append(0x20)
    message.append(0x40)
    #puts each channel value in little endian format in the message
    for channel in channels:
        message.append(channel%256)
        message.append(channel//256)
    #calculates and ands the required cheksum
    msgsum=0
    for i in message:
        msgsum+=i
    checksum = 0xffff-msgsum
    message.append(checksum%256)
    message.append(checksum//256)
    #ensures each of the two parts of each channel is 1 byte by converting it to
    #a char
    return message #list(map(lambda i :struct.pack(b'B',i),message))

def commands(channels):
    """This function takes a list of values of max length 14 and sends it
    in the correct form to the flight controller. Gives the neutral value of 0x05DC
    (1500) to the unused channels"""
    command = []
    for i in channels:
        command.append(i)
    command+=([0x05dc]*(14-len(channels)))
    message = pack(command)
    with connecttoport('/dev/ttyS0') as port:
        send(message, port)

def dronecontrol(roll, pitch, throttle, yaw):
    """Master function which will let you asign the roll, pitch, throtle and yaw
    values"""
    values = [roll, pitch, throttle, yaw]
    commands(values)

def test():
    commands([1000]*4)
    print("start")
    port = serial.Serial('/dev/ttyS0',115200, timeout=10, write_timeout=10 )
    port.write(struct.pack(b'B',128))
    print("end")
    port=connecttoport('/dev/ttyS0')
    channel = [1000]*14
    message = pack(channel)
    for i in range(2000):
        send(message, port)
        sleep(0.01)
if __name__ == "__main__":
    test()
