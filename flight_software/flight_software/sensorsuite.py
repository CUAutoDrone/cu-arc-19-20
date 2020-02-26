from ultrasonic import Ultrasonic
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

class SensorSuite:
    """This is a class that will get all the sensor information that we need
    """

    def __init__(self):
        self.connected = False

        self.x = 0
        self.y = 0
        self.z = 0

        self.ultrasonic = None


    def get_position(self):
        return (self.x, self.y, self.z)


    def update_z(self):
        while self.ultrasonic:
            self.z = self.ultrasonic.measure()
            sleep(0.01)


    def connect(self):
        self.connected = True
        self.ultrasonic = Ultrasonic()

        Thread(target=self.update_z).start()


    def disconnect(self):
        self.connected = False

        self.ultrasonic.disconnect()
        self.ultrasonic = None


def test():
    s = SensorSuite()
    s.connect()

    for i in range(10):
        print(s.get_position())
        sleep(0.1)

    s.disconnect()

if __name__ == "__main__":
    test()
