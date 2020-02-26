from time import time, sleep
import RPi.GPIO as GPIO

class Ultrasonic:

    MS_TO_CM = 17150

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.pin = 12

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

        sleep(0.01)


    def measure(self):

        GPIO.output(self.pin, True)
        sleep(0.00001)
        GPIO.output(self.pin, False)

        GPIO.setup(self.pin, GPIO.IN)

        while GPIO.input(self.pin) == 0:
            pass

        start = time()

        while GPIO.input(self.pin) == 1:
            pass

        elapsed = time() - start

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)

        return elapsed * Ultrasonic.MS_TO_CM


    def disconnect(self):
        GPIO.cleanup()


def test():
    us = Ultrasonic()
    for i in range(10):
        print(us.measure())
        sleep(0.1)
    us.disconnect()


if __name__ == '__main__':
    test()
