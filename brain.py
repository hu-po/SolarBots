# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Definitions for all parameters, runs/calls all other functions

import serial
import numpy as np
from Sensor import Sensor
from PinMaster import PinMaster
from Parameters import Parameters
import math
import sys

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Create Parameters object
params = Parameters()

# Add Navigation Parameters (name, value, description)
params.addParam('DATA_SAMPLE_SIZE', 3, 'Sample size for data (increase to stabilize at cost of speed)')
params.addParam('MAX_ITER', 10, 'Maximum number of Sense-Plan-Act Cycles')
params.addParam('MOVE_PER_TURN', 1, 'How far you want the robot to move each step (increments of 10cm)')
params.addParam('TIMEOUT', 0.1, 'How many seconds until sensor loop times out and returns a bunch of zeros')
params.addParam('FORWARD_VECTOR', [0, 1, 0], 'Describes the forward (Theta = 0) direction in the robot frame')

# Add SLAM Parameters (name, value, description)
params.addParam('RAND_DIST_MU', 0, 'Center of distribution (cm)')
params.addParam('RAND_DIST_SIGMA', 1, 'Standard deviation (cm)')
params.addParam('RAND_ANG_MU', 0, 'Degrees')
params.addParam('RAND_ANG_SIGMA', 10, 'Degrees')
params.addParam('RAND_NUM', 10, 'Number of random samples')

# Add Kalman Filter Parameters
params.addParam('OBSERVATION_NOISE', 0.1, 'Kalman Filter observation noise')

# Add Tuning Parameters
params.addParam('DISTANCE_WEIGHT', [1, 1, 0.2],
                'Weighting of [X, Y, Theta] each when determining distance metric')
params.addParam('FOG_RADIUS', 100,
                'Distance metric to use (centered around current position) for looking for close nodes')

# Add file path parameters
params.addParam('ROOM_PATH', 'Data/Rooms/', 'Path to saved room objects')

# Add Motor Parameters
params.addParam('SEC_PER_TURN', 10, 'Seconds required to complete one full turn')
params.addParam('SEC_PER_MOVE', 1, 'Seconds required to move 10cm')
params.addParam('MOTOR_DEFAULT_PWR', 50, 'Default starting power for the motor')
params.addParam('MOTOR_OFFSET_PWR', -1, 'Difference between Motor 1 and Motor 2')
params.addParam('MOTOR_PWM_FREQ', 357, 'Frequency of PWM for motors')
params.addParam('MOTOR_PWR', 50, '0 - 100 speed of motor')

# Add Camera Parameters
params.addParam('CAMERA_SERVOS',
                [[0, 0], [70, 0], [110, 0], [0, 70], [0, 110]],
                'Position of servos for pictures, Note: Size determines number of pictures')

# Create Sensor object
sensors = Sensor()

# Add sensors to sensor dictionary
sensors.addSensor('HC-SR04', 1, 10, [0,    8.5,  0,     math.pi / 2])
sensors.addSensor('HC-SR04', 2, 10, [7.36,   4.25,  0,     math.pi / 6])
sensors.addSensor('HC-SR04', 3, 10, [7.36,  -4.25,  0,    -math.pi / 6])
sensors.addSensor('HC-SR04', 4, 10, [0,   -8.5,  0,    -math.pi / 2])
sensors.addSensor('HC-SR04', 5, 10, [-7.36,  -4.25,  0, -5 * (math.pi / 6)])
sensors.addSensor('HC-SR04', 6, 10, [-7.36,   4.25,  0,  5 * (math.pi / 6)])
sensors.addSensor('TSL2561', 1, 5, [0,    8.5,  0, 0,     math.pi / 6])
sensors.addSensor('TSL2561', 2, 5, [0,    8.5,  0, 0,    -math.pi / 2])
sensors.addSensor('TSL2561', 3, 5, [0,    8.5,  0, 0,  5 * (math.pi / 6)])

# Create PinMaster object
pins = PinMaster()

# Add pins to pin dictionary
pins.addPin('MOTOR1A', 18)
pins.addPin('MOTOR1B', 23)  # Right Motor
pins.addPin('MOTOR1E', 24)
pins.addPin('MOTOR2A', 17)  # Left Motor
pins.addPin('MOTOR2B', 27)
pins.addPin('MOTOR2E', 22)
pins.addPin('SERVO1',  5)  # Horizontal (Side to Side) servo
pins.addPin('SERVO2', 13)  # Vertical (Up and Down) servo
pins.addPin('BUZZER', 4)   # Piezo buzzer

# # Create Map object
# mapa = Mapa()


def main():

    print "Importing functions ..."

    # from python_mysql_connect import connect, insert_current_pos, query_current_pos
    from motor import GPIOclean
    from Room import Room
    import navigation
    # from maptool import pull_map
    # from slam import slamfunc

    # print "Connecting to database ..."
    # connect()

    # print "Downloading map from database ..."
    # pull_map()

    room = Room()
    if len(sys.argv) > 1:
        print "Loading up Room: " + str(sys.argv[1])
        room.load_room()
    else:
        print "No Room specified, using empty Room ..."

    print "Starting main exploration loop ..."

    for i in range(0, params.p['MAX_ITER']):

        # Explore (Move to a new area)
        new_area = navigation.explore()

        # Add area to room object
        room.areas.append(new_area)

    print "Exited main exploration loop ..."

    print "Storing room to file..."
    room.store_room()

    # print "Pushing map to database ..."
    # push_map()

    print "Clean up motor GPIO ..."
    GPIOclean()


if __name__ == '__main__':
    main()

# --------------------- OLD CODE

        # Get current robot pose from database
        # curr_pos = query_current_pos()

        # Move robot to new position based on current position and sensor input
        # curr_input = navigate(curr_pos)

        # Use current position and explore dataset to determine new location
        # curr_pos_slam = slamfunc(scan, curr_pos)

        # Feed SLAM estimate of position into Kalman Filter
        # curr_pos_filter = kalman(curr_pos, curr_pos_slam, curr_input)

        # curr_pos_filter = kalman(curr_pos, curr_pos, curr_input)

        # print curr_pos # Last known filtered state of robot
        # print curr_meas # Current approximate state of robot
        # print curr_input # Input vector which was inputed since last known state
        # print curr_pos_filter # New filtered state of robot

        # Push new robot pose to database
        # insert_current_pos(curr_pos_filter)
