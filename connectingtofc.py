import serial

def connecttoport(dport):
    port= serial.Serial(dport,15200, timeout=1,write_timeout=1)
    print("Desired port is "+port.name)
    return port
def send(dmsg, port):
    port.write(dmsg)
def pack(channels):
    message=[]
    message.append(0x20)
    message.append(0x40)
    for channel in channels:
        message.append(channel%256)
        message.append(channel//256)
    #begins the sum needed to create the checksum bytes Not use if this should be
    #0x4020 instead
    msgsum=0
    for i in message:
        msgsum+=i
    cheksum = 0xfff-msgsum
    message.appned(checksum%256)
    message.appned(checksum//256)

def test():
    pass
