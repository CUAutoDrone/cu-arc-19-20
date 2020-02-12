#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import struct
from time import sleep
from threading import Thread

class FlightController:
    """Representation of the flight controller.


    Attributes
    ----------
    connection : serial.Serial
        The serial connection to the flight controller. None until initialized.

    port : string
        The port of the serial conection.

    baudrate : int
        The baudrate of the serial connection.

    timeout : int
        The maximum alowable time in seconds to wait for a message.

    position : (float, float, float)
        The current position of the drone relative to the start position (or to
        the last zeroed postion).

    armed : bool
        The arm status of the flight controller.

    throttle : float
        The current value of the throttle signal being sent to the drone.
        In range (0, 100)

    pitch : float
        The current value of the pitch signal being sent to the drone.
        In range (-100, 100)

    roll : float
        The current value of the roll signal being sent to the drone.
        In range (-100, 100)

    yaw : float
        The current value of the yaw signal being sent to the drone.
        In range (-100, 100)

    """

    def __init__(self, port='/dev/ttyS0', baudrate=115200, timeout=1):
        """Constructor method
        """
        self.connection = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.position = (0,0,0)

        self.armed = False
        self.throttle = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0


    @staticmethod
    def pack(channels):
        """Pack message in iBus protocol.

        Parameters
        ----------
        channels : short array
        """
        message=[]

        #add the header of the message
        message.append(0x20)
        message.append(0x40)

        #put each channel value in little endian format in the message
        for channel in channels:
            message.append(channel % 256)
            message.append(channel // 256)

        #pad message to required size
        message += [220, 5] * (14 - len(channels))

        #calculate and add checksum
        checksum = 0xFFFF - sum(message)
        message.append(checksum % 256)
        message.append(checksum // 256)
        return message


    def send(self, msg):
        """Send a message to the flight controller.

        Parameters
        ----------
        msg : byte array
            The message to be sent.

        Raises
        ------
        ValueError
            Raised when there is no connection to the flight controller.
        """
        if self.connection:
            self.connection.write(msg)
        else:
            raise ValueError("no connection")


    def signal_loop(self):
        while self.connection:
            self.send(self.pack([
                self.pitch,
                self.roll,
                self.yaw,
                self.throttle,
                1500,
                1900 if self.armed else 1500
            ]))
            sleep(0.01)


    def connect(self):
        """Connect to the flight controller, and start signal loop thread.

        Raises
        ------
        SerialException
            Raised when the connection fails
        """
        if not self.connection:
            self.connection = serial.Serial(self.port,
                                            self.baudrate,
                                            timeout=self.timeout)

            sig = Thread(target=self.signal_loop)
            sig.start()

    def arm(self):
        self.armed = True


    def disarm(self):
        self.armed = False


    def disconnect(self):
        """Disconnect from the flight controller and end signal loop thread.
        """
        self.connection = None


def _test():
    fc = FlightController()
    fc.connect()
    fc.arm = True


if __name__ == "__main__":
    _test()
