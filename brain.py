# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Definitions for all parameters, runs/calls all other functions

print "Importing functions ..."

import math
import sys
import serial
import numpy as np

from Sensor import Sensor
from PinMaster import PinMaster
from Parameters import Parameters

# ----------------------------------------------------
#           INITIALIZE GLOBAL VARIABLES
# ----------------------------------------------------

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Create Parameters object
params = Parameters()

# Add Navigation Parameters (name, value, description)
params.addParam('DATA_SAMPLE_SIZE', 3, 'Sample size for data (increase to stabilize at cost of speed)')
params.addParam('MAX_ITER', 10, 'Maximum number of Sense-Plan-Act Cycles')
params.addParam('MOVEMENT_WEIGHT', 5.0, 'Weight factor for movement vector vs move units to be traveled')
params.addParam('TIMEOUT', 0.1, 'How many seconds until sensor loop times out and returns a bunch of zeros')
params.addParam('FORWARD_VECTOR', [0, 1, 0], 'Describes the forward (Theta = 0) direction in the robot frame')
params.addParam('BACKWARD_VECTOR', [0, -1, 0], 'Describes the backwards (Theta = 0) direction in the robot frame')
params.addParam('WAIT_TIME', 2, 'How many seconds in between exploration steps')

# Add Tuning Parameters
params.addParam('DISTANCE_WEIGHT', [0.1, 0.1, 0.2],
                'Weighting of [X, Y, Theta] each when determining distance metric')

# Add Motor Parameters
params.addParam('SEC_PER_TURN', 2.8, 'Seconds required to turn 1 unit')
params.addParam('SEC_PER_MOVE', 1.0, 'Seconds required to move 1 unit')
params.addParam('DIST_PER_MOVE', 10.0, 'Centimeters in 1 move unit')
params.addParam('DEG_PER_TURN', 2*math.pi, 'Radians in 1 turn unit')
params.addParam('MOTOR_DEFAULT_PWR', 30, 'Default starting power for the motor')
params.addParam('MOTOR_OFFSET_PWR', 0, 'Difference between Motor 1 and Motor 2')
params.addParam('MOTOR_PWM_FREQ', 357, 'Frequency of PWM for motors')
params.addParam('MOTOR_PWR', 30, '0 - 100 speed of motor')

# Create Sensor object
sensors = Sensor()

# Add sensors to sensor dictionary
# 'Name', number, weight (higher is more important), location
sensors.addSensor('HC-SR04', 1, 2, [0,    8.5,  0,     math.pi / 2])
sensors.addSensor('HC-SR04', 2, 2, [7.36,   4.25,  0,     math.pi / 6])
sensors.addSensor('HC-SR04', 3, 2, [7.36,  -4.25,  0,    -math.pi / 6])
sensors.addSensor('HC-SR04', 4, 2, [0,   -8.5,  0,    -math.pi / 2])
sensors.addSensor('HC-SR04', 5, 2, [-7.36,  -4.25,  0, -5 * (math.pi / 6)])
sensors.addSensor('HC-SR04', 6, 2, [-7.36,   4.25,  0,  5 * (math.pi / 6)])
sensors.addSensor('TSL2561', 1, 1, [7.36,   4.25,  0,     math.pi / 6])
sensors.addSensor('TSL2561', 2, 1, [0,   -8.5,  0,    -math.pi / 2])
sensors.addSensor('TSL2561', 3, 1, [-7.36,   4.25,  0,  5 * (math.pi / 6)])

# Create PinMaster object
pins = PinMaster()

# Add pins to pin dictionary
pins.addPin('MOTOR1A', 18) # 16)
pins.addPin('MOTOR1B', 23) # 20)  # Right Motor
pins.addPin('MOTOR1E', 24) # 21)
pins.addPin('MOTOR2A', 17) # 13)  # Left Motor
pins.addPin('MOTOR2B', 27) # 19)
pins.addPin('MOTOR2E', 22) # 26)
pins.addPin('BUZZER', 4) #25)  # Piezo buzzer