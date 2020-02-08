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
    message.append(0x20)
    message.append(0x40)
    for channel in channels:
        message.append(channel%256)
        message.append(channel//256)
    msgsum=0
    for i in message:
        msgsum+=i
    checksum = 0xffff-msgsum
    message.append(checksum%256)
    message.append(checksum//256)

    return list(map(lambda i :struct.pack(b'B',i),message))
def commands(channels):
    """This function will take any amount of channels given and both pack and send
    the message to the flight controller. Values given must still be given in the
    order of the channels"""
    command = []
    for i in channels:
        command.append(i)
    command+=([0x05dc]*(14-len(channels)))
    message = pack(command)
    with connecttoport('/dev/ttyS0') as port:
        send(message, port)
def test():
    pass
    #commands([1000]*4)
    # print("start")
    # port = serial.Serial('/dev/ttyS0',115200, timeout=10, write_timeout=10 )
    # port.write(struct.pack(b'B',128))
    # print("end")
    # port=connecttoport('/dev/ttyS0')
    # channel = [1000]*14
    # message = pack(channel)
    # for i in range(2000):
    #     send(message, port)

if __name__ == "__main__":
    #test()
    pass
