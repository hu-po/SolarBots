# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains the camera servo functions for the robot

import RPi.GPIO as GPIO
import numpy as np
from brain import Servo1, Servo2

# Sets the angle for a desired servo
def setServo(int servo_num, int angle):
	return

# Gets current angle for a desired servo
def getServo(int servo_num):
	return

def main():

	# Test out functionality
	setServo(1, 0)
    sleep(1)

    setServo(1, 90)
    sleep(1)

    setServo(1, 100)
    sleep(1)

	setServo(2, 0)
    sleep(1)

    setServo(2, 90)
    sleep(1)

    setServo(2, 100)
    sleep(1)  

if __name__ == '__main__':
    main()

