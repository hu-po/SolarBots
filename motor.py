# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains all the low level motor/move functions for the robot

from time import sleep
import RPi.GPIO as GPIO
from brain import params, pins

# Initialize and setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setup motor pin output
GPIO.setup(pins.p['MOTOR1A'], GPIO.OUT)
GPIO.setup(pins.p['MOTOR1B'], GPIO.OUT)
GPIO.setup(pins.p['MOTOR1E'], GPIO.OUT)
GPIO.setup(pins.p['MOTOR2A'], GPIO.OUT)
GPIO.setup(pins.p['MOTOR2B'], GPIO.OUT)
GPIO.setup(pins.p['MOTOR2E'], GPIO.OUT)

# Output low signal
GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)
GPIO.output(pins.p['MOTOR1E'], GPIO.LOW)
GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)
GPIO.output(pins.p['MOTOR2E'], GPIO.LOW)

# Initialize PWM for  both motors
E1 = GPIO.PWM(pins.p['MOTOR1E'], params.p['MOTOR_PWM_FREQ'])
E2 = GPIO.PWM(pins.p['MOTOR2E'], params.p['MOTOR_PWM_FREQ'])


# Change speed of motor by controlling duty cycle
# def speed(num):
#     E1.ChangeDutyCycle(num)
#     E2.ChangeDutyCycle(num + MOTOR_OFFSET_PWR)
#     return


def moveBot(direction, distance=0, num=params.p['MOTOR_DEFAULT_PWR'], continuous_mode=False):

    # Start both sowftware PWMs
    E1.start(num)
    E2.start(num + params.p['MOTOR_OFFSET_PWR'])

    # Alternatively send a HIGH signal for 100%
    # GPIO.output(Motor1E, GPIO.HIGH)
    # GPIO.output(Motor2E, GPIO.HIGH)

    # # Debug print
    # print continuous_mode

    if direction == 'forward':
        print "Going forwards ..."

        GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
        GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

        GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
        GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

        if not continuous_mode:
            sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

    elif direction == 'backward':
        print "Going backwards ..."

        GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

        GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

        if not continuous_mode:
            sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

    elif direction == 'left':
        print "Turning Left ..."

        GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
        GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

        GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

        if not continuous_mode:
            sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

    elif direction == 'right':
        print "Turning Right ..."

        GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

        GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
        GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

        if not continuous_mode:
            sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

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

    GPIO.output(pins.p['MOTOR1E'], GPIO.LOW)
    GPIO.output(pins.p['MOTOR2E'], GPIO.LOW)


def main():

    sleep(1)

    moveBot('forward', 1, params.p['MOTOR_DEFAULT_PWR'])  # Move forward 1 unit (10 cm)

    sleep(1)

    moveBot('left', 90, params.p['MOTOR_DEFAULT_PWR'])  # Make a 90 degree turn

    sleep(1)

    moveBot('forward', 1, params.p['MOTOR_DEFAULT_PWR'])

    sleep(1)

    moveBot('right', 90, params.p['MOTOR_DEFAULT_PWR'])

    GPIOclean()

if __name__ == '__main__':
    main()
