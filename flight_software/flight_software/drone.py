#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from time import sleep
from threading import Thread

class Drone:
    """Representation of the drone.


    Attributes
    ----------
    connection : serial.Serial
        The serial connection to the flight controller. None until initialized.

    port : string
        The port of the serial conection.

    baudrate : int
        The baudrate of the serial connection.

    timeout : int
        The maximum allowable time in seconds to wait for a message.

    position : (float, float, float)
        The current position of the drone relative to the start position (or to
        the last zeroed postion).

    waypoint : (float, float, float)
        The target position of the drone relative to the start position (or to
        the last zeroed postion).

    armed : bool
        The arm status of the flight controller.

    throttle : float
        The current value of the throttle signal being sent to the flight
        controller. In range (0, 100)

    pitch : float
        The current value of the pitch signal being sent to the flight
        controller. In range (-100, 100)

    roll : float
        The current value of the roll signal being sent to the flight
        controller. In range (-100, 100)

    yaw : float
        The current value of the yaw signal being sent to the flight
        controller. In range (-100, 100)

    """


    def __init__(self, port='/dev/ttyS0', baudrate=115200, timeout=1):
        """Constructor method
        """
        self.connection = None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.position = (0, 0, 0)
        self.waypoint = (0, 0, 0)

        self.armed = False
        self.throttle = 0
        self.pitch = 1500
        self.roll = 1500
        self.yaw = 1500


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


    def position_loop(self):
        while self.connection:
            (x, y, z) = self.position

            #TODO: update position with sensor data
            self.position = (
                x,
                y,
                z
            )
            sleep(0.01)


    def connect(self):
        """Connect to the flight controller and start signal loop and position
        calculation threads.

        Raises
        ------
        SerialException
            Raised when the connection fails
        """
        if not self.connection:
            self.connection = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )

            Thread(target=self.signal_loop).start()
            Thread(target=self.position_loop).start()


    def arm(self):
        """Arm the drone.
        """
        self.armed = True


    def set_waypoint(x, y, z):
        """ Set the target position of the drone in meters offset from start.

        Parameters
        ----------
        x : float
            The x-coordinate of the target position.

        y : float
            The y-coordinate of the target position.

        z : float
            The z-coordinate of the target position.
        """
        self.waypoint = (x, y, z)


    def disarm(self):
        """Disarm the drone.
        """
        self.armed = False


    def disconnect(self):
        """Disconnect from the flight controller and end signal loop thread.
        """
        if self.connection:
            self.connection.close()
            self.connection = None


def _test():
    fc = Drone()

    fc.connect()
    sleep(1)
    fc.arm()
    sleep(1)
    fc.throttle = 1000
    sleep(1)
    fc.throttle = 0
    sleep(1)
    fc.disarm()
    sleep(1)
    fc.disconnect()


if __name__ == "__main__":
    _test()
