# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains the camera servo functions for the robot

import RPi.GPIO as GPIO
import numpy as np
from brain import Servo1, Servo2

class Servo(object):

    def __init__(self, servo_num):
        GPIO.setmode(GPIO.BCM)
        self.servo_num = servo_num
        self.servi_step = params.p('CAMERA_SERVO_STEP')
        self.servo_pin = pins.p(''.join(['SERVO', self.servo_num]))
        GPIO.setup(self.servo_pin, GPIO.IN)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        print "Servo " + str(self.servo_num) + " ready"

    def __del__(self):
        print "Servo " + str(self.servo_num) + " done"

    # Sets the angle for a desired servo
    def setServo(angle):


    # Gets current angle for a desired servo
    def getServo():

        return angle


if __name__ == "__main__":

    # Create Servo object and test it out
    servo1 = Servo(1)
    servo1.setServo(20)
    servo1.setServo(40)

    # Create Servo object and test it out
    servo2 = Servo(2)
    servo2.setServo(20)
    servo2.setServo(40)