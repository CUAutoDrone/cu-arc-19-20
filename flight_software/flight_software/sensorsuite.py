from getdist import measure
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

    def get_position(self):
        return (self.x, self.y, self.z)

    def ultrasonic(self):
        while self.connected:
            self.z = measure()
            sleep(0.01)

    def connect(self):
        self.connected = True
        Thread(target=self.ultrasonic).start()

    def disconnect(self):
        self.connected = False
        GPIO.cleanup()

def test():
    di = SensorSuite()
    di.connect()
    try:
        while True:
            print(di.z)
            sleep(1)
    except KeyboardInterrupt:
        di.connected = False

if __name__ == "__main__":
    test()
