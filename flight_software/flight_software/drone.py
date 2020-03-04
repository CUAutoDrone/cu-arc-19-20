#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sensorsuite import SensorSuite
import serial
from time import sleep, time
from threading import Thread
from operator import add, sub

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

        self.waypoint = (0, 0, 0)

        self.armed = False
        self.throttle = 0
        self.pitch = 1500
        self.roll = 1500
        self.yaw = 1500

        self.sensors = None


    @staticmethod
    def pack(channels):
        """Pack message in iBus protocol.

        Parameters
        ----------
        channels : short array

        Requires
        --------
        channels has length strictly less than 15.
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
        bound = lambda n, l, u : l if n < l else u if n > u else n
        p = (0, 0, 1)
        i = (0, 0, 0)
        i_state = (0, 0, 0)
        d = (0, 0, 0)
        old_error = (0, 0, 0)

        while self.connection:
            #TODO: pid loop to hold waypoint.
            error = tuple(map(sub, self.waypoint, self.sensors.get_position()))
            bounded_error = tuple(map(lambda x : bound(x, -1000, 1000), error))

            self.throttle = int(max(sum([
                p[2] * error[2],
                i[2] * i_state[2],
                d[2] * (error[2] - old_error[2])
            ]), 0))

            i_state = tuple(map(add, i_state, bounded_error))
            old_error = error
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

        if not self.sensors:
            self.sensors = SensorSuite()
            self.sensors.connect()

            Thread(target=self.position_loop).start()


    def arm(self):
        """Arm the drone.
        """
        self.armed = True


    def set_waypoint(self, x, y, z):
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
            c = self.connection
            self.connection = None
            sleep(0.1)
            self.sensors.disconnect()
            c.close()


def _test():
    try:
        d = Drone()
        d.connect()

        for i in range(5):
            print(d.sensors.get_position(), d.throttle)
            sleep(1)

        d.set_waypoint(0, 0, 100)

        for i in range(5):
            print(d.sensors.get_position(), d.throttle)
            sleep(1)

        d.disconnect()

    except KeyboardInterrupt:
        d.disconnect()

if __name__ == "__main__":
    _test()
