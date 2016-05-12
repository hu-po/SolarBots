# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains all the low level motor/move functions for the robot

from time import sleep
import RPi.GPIO as GPIO
from brain import params, pins
import logging
import math

# Initialize and setup GPIO
GPIO.setmode(GPIO.BCM)

class Motor(object):

    def __init__(self):
        '''
            Initializes motor object, setting pins and starting PWMs
        '''

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
        self.E1 = GPIO.PWM(pins.p['MOTOR1E'], params.p['MOTOR_PWM_FREQ'])
        self.E2 = GPIO.PWM(pins.p['MOTOR2E'], params.p['MOTOR_PWM_FREQ'])

        # Change speed of motor by controlling duty cycle
        # def speed(num):
        #     E1.ChangeDutyCycle(num)
        #     E2.ChangeDutyCycle(num + MOTOR_OFFSET_PWR)
        #     return


    def move_bot(self, direction, distance=0, num=params.p['MOTOR_DEFAULT_PWR'], continuous_mode=False):
        '''
            Moves the robot (runs motors) given motion primitives
        '''

        # Start both sowftware PWMs
        self.E1.start(num)
        self.E2.start(num + params.p['MOTOR_OFFSET_PWR'])

        # Alternatively send a HIGH signal for 100%
        # GPIO.output(Motor1E, GPIO.HIGH)
        # GPIO.output(Motor2E, GPIO.HIGH)

        # # Debug print
        # logger.debug('Continuous_mode: ', continuous_mode)

        if direction == 'forward':
            # logger.info('Going forwards ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

            GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

            if not continuous_mode:
                sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

        elif direction == 'backward':
            # logger.info('Going backwards ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

            GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

            if not continuous_mode:
                sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

        elif direction == 'left':
            # logger.info('Turning Left ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

            GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

            if not continuous_mode:
                sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

        elif direction == 'right':
            # logger.info('Turning Right ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

            GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

            if not continuous_mode:
                sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

        else:
            print "ERROR: Wrong direction input"

        if not continuous_mode:

            # Stop motors by outputting low signal
            print "Stopping Motors..."
            GPIO.output(pins.p['MOTOR1E'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR2E'], GPIO.LOW)

        return

    def stop_bot(self):
        '''
            Stop method kills PWMs and stops motors
        '''

        # Stop PWMs
        print "Stopping PWMs..."
        self.E1.stop()
        self.E2.stop()

        # Stop motors by outputting low signal
        print "Stopping Motors..."
        GPIO.output(pins.p['MOTOR1E'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR2E'], GPIO.LOW)

        # Clean any loose ends in the GPIO
        print "Clean up GPIO ..."
        GPIO.cleanup()

# Testing code, run with: python navigation.py
if __name__ == '__main__':

    # Create motor object
    move = Motor()

    sleep(1)

    move.moveBot('forward', 1, params.p['MOTOR_DEFAULT_PWR'])  # Move forward 1 unit (10 cm)

    sleep(1)

    move.moveBot('left', (2.0 * math.pi), params.p['MOTOR_DEFAULT_PWR'])  # Make a 360 degree turn

    sleep(1)

    move.moveBot('forward', 1, params.p['MOTOR_DEFAULT_PWR'])

    sleep(1)

    move.moveBot('right', (2.0 * math.pi), params.p['MOTOR_DEFAULT_PWR']) # Make a 360 degree turn

    del move
