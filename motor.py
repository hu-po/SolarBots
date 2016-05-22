# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains all the low level motor/move functions for the robot

from time import sleep
import RPi.GPIO as GPIO
from brain import params, pins
import logging
import math

import Move

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
        self.E1 = GPIO.PWM(pins.p['MOTOR1E'], params.p['MOTOR_DEFAULT_PWM_FREQ'])
        self.E2 = GPIO.PWM(pins.p['MOTOR2E'], params.p['MOTOR_DEFAULT_PWM_FREQ'])

    def change_dc(self, new_dc):
        '''
            Change dc (duty cycle) of the motor (0 - 100)
        '''
        self.E1.ChangeDutyCycle(new_dc[0])
        self.E2.ChangeDutyCycle(new_dc[1])
        
    def change_freq(self, new_freq):
        '''
            Change frequency of the motor PWM
        '''
        self.E1.ChangeFrequency(new_freq[0])
        self.E2.ChangeFrequency(new_freq[1])

    def e_brake(self):
        '''
            Stop motors by outputting low signal
        '''
        print "Stopping Motors..."
        GPIO.output(pins.p['MOTOR1E'], GPIO.LOW)
        GPIO.output(pins.p['MOTOR2E'], GPIO.LOW)

    def nitro_boost(self):
        '''
            Runs motor at highest power by outputting high signal
        '''
        GPIO.output(pins.p['MOTOR1E'], GPIO.HIGH)
        GPIO.output(pins.p['MOTOR2E'], GPIO.HIGH)

    def move_bot(self, direction, distance=0, dc=params.p['MOTOR_DEFAULT_PWM_DC'], continuous_mode=False):
        '''
            Moves the robot (runs motors) given motion primitives
        '''

        # Start both sowftware PWMs (dc is the duty cycle)
        self.E1.start(dc)
        self.E2.start(dc)

        # # Debug print
        # print('Continuous_mode: ', continuous_mode)

        if direction == Move.FORWARD:
            # print('Going forwards ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

            GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

            if not continuous_mode:
                sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

        elif direction == Move.BACKWARD:
            # print('Going backwards ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

            GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

            if not continuous_mode:
                sleep((distance / params.p['DIST_PER_MOVE']) * params.p['SEC_PER_MOVE'])

        elif direction == Move.LEFT:
            # print('Turning Left ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR1B'], GPIO.LOW)

            GPIO.output(pins.p['MOTOR2A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR2B'], GPIO.HIGH)

            if not continuous_mode:
                sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

        elif direction == Move.RIGHT:
            # print('Turning Right ...')

            GPIO.output(pins.p['MOTOR1A'], GPIO.LOW)
            GPIO.output(pins.p['MOTOR1B'], GPIO.HIGH)

            GPIO.output(pins.p['MOTOR2A'], GPIO.HIGH)
            GPIO.output(pins.p['MOTOR2B'], GPIO.LOW)

            if not continuous_mode:
                sleep((distance / params.p['DEG_PER_TURN']) * params.p['SEC_PER_TURN'])

        else:
            print "ERROR: Wrong direction input"

        if not continuous_mode:
            self.e_brake()

        return

    def stop_bot(self):
        '''
            Stop method kills PWMs and stops motors
        '''

        # Stop PWMs
        print "Stopping PWMs..."
        self.E1.stop()
        self.E2.stop()

        # Kill motors just to be sure
        self.e_brake()

        # # Clean any loose ends in the GPIO
        # print "Clean up GPIO ..."
        # GPIO.cleanup()

# Testing code, run with: python motor.py
if __name__ == '__main__':

    # Create motor object
    move = Motor()

    # Move robot back and forth for testing and tuning
    move.moveBot('forward', 1)  # Move forward 1 unit (10 cm)
    sleep(1)
    move.moveBot('left', 2*math.pi)  # Make a 360 degree turn
    sleep(1)
    move.moveBot('backwards', 1)
    sleep(1)
    move.moveBot('right', 2*math.pi) # Make a 360 degree turn
