import getdist
from threading import Thread
from time import sleep

 class SensorSuite:
    """This is a class that will get all the sensor information that we need
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def get_position(self):
        return (self.x, self.y, self.z)

    def ultrasonic(self):
        self.z = measure()
        sleep(0.01)

    def connnect(self):
        Thread(target=self.ultrasonic).start()

def test():
    di = SensorSuite()
    di.connect()
    while True:
        print(di.z)
        sleep(1)

if __name__ == "__main__":
    test()
