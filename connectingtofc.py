import serial

def connecttoport(dport):
    """This function connect to the desired port"""
    port= serial.Serial(dport,15200, timeout=1,write_timeout=1)
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
    checksum = 0xfff-msgsum
    message.append(checksum%256)
    message.append(checksum//256)
    return message

def test():
    channel = [1000]*14
    port=connecttoport('/dev/ttyAMA0')
    message = pack(channel)
    send(message, port)

if __name__ == "__main__":
    test()
