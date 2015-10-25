# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains all the low level motor/move functions for the robot

from time import sleep
import RPi.GPIO as GPIO
from brain import SEC_PER_TURN, SEC_PER_MOVE, MOTOR_DEFAULT_PWR, MOTOR_OFFSET_PWR, Motor1A, Motor1B, Motor1E, Motor2A, Motor2B, Motor2E

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

# Setup motor pin output
GPIO.setup(Motor1A, GPIO.OUT)  # Left Motor
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

# Output low signal
GPIO.output(Motor1A, GPIO.LOW)  # Right Motor
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2A, GPIO.LOW)
GPIO.output(Motor2B, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)

# Initialize PWM for  both motors
E1 = GPIO.PWM(Motor1E, 100)
E2 = GPIO.PWM(Motor2E, 100)


# Change speed of motor by controlling duty cycle
# def speed(num):
#     E1.ChangeDutyCycle(num)
#     E2.ChangeDutyCycle(num + MOTOR_OFFSET_PWR)
#     return


def moveBot(direction, distance=10, num=MOTOR_DEFAULT_PWR, continuous_mode=False):

    # Start both sowftware PWMs
    E1.start(num)
    E2.start(num + MOTOR_OFFSET_PWR)

    # Alternatively send a HIGH signal for 100%
    # GPIO.output(Motor1E, GPIO.HIGH)
    # GPIO.output(Motor2E, GPIO.HIGH)

    print continuous_mode

    if direction == 'forward':
        print "Going forwards ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)

        if not continuous_mode:
            sleep(distance * SEC_PER_MOVE)

    elif direction == 'backward':
        print "Going backwards ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)

        if not continuous_mode:
            sleep(distance * SEC_PER_MOVE)

    elif direction == 'turnleft':
        print "Turning Left ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)

        if not continuous_mode:
            sleep((distance / 360.0) * SEC_PER_TURN)

    elif direction == 'turnright':
        print "Turning Right ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)

        if not continuous_mode:
            sleep((distance / 360.0) * SEC_PER_TURN)

    else:
        print "ERROR: Wrong direction input"

    if not continuous_mode:
        motorStop()

    return


def GPIOclean():  # Cleanup GPIO output
    GPIO.cleanup()


def motorStop():    # Stop motors
    print "Stopping ..."

    E1.stop()
    E2.stop()

    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)

    return


def main():

    sleep(1)

    moveBot('forward', 1, MOTOR_DEFAULT_PWR)  # Move forward 1 unit (10 cm)

    sleep(1)

    moveBot('turnleft', 90, MOTOR_DEFAULT_PWR)  # Make a 90 degree turn

    sleep(1)

    moveBot('forward', 1, MOTOR_DEFAULT_PWR)

    sleep(1)

    moveBot('turnright', 90, MOTOR_DEFAULT_PWR)

    GPIOclean()

if __name__ == '__main__':
    main()
