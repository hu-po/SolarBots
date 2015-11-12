# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Definitions for all parameters, runs/calls all other functions

import serial
import numpy as np
import Sensor
import math

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Define Navigation Parameters
# Sample size for data (increase to stabilize at cost of speed)
DATA_SAMPLE_SIZE = 3
# Number of sonar sensors #TODO: figure this out based on SENSOR_POS
NUM_SONAR = 6
# Number of light sensors #TODO: figure this out based on SENSOR_POS
NUM_LIGHT = 3
MAX_ITER = 10   # Maximum number of Sense-Plan-Act Cycles
MOTOR_PWR = 30  # 0 - 100 speed of motor
EXPLORE_ITER = 4  # Number of sensor readings in an explore scan
EXPLORE_ANGLE = 360.0  # Angle to explore during an explore scan

# Define SLAM Parameters (distance/angle perturbations)
# Radius of section of map to use (centered around current position) for SLAM
FOG_RADIUS = 100
RAND_DIST_MU = 0  # Center of distribution (cm)
RAND_DIST_SIGMA = 1  # Standard deviation (cm)
RAND_ANG_MU = 0  # Degrees
RAND_ANG_SIGMA = 10  # Degrees
RAND_NUM = 10  # Number of random samples

# Define Kalman Filter Parameters
OBSERVATION_NOISE = 0.1

# Define Motor Parameters
SEC_PER_TURN = 10   # Seconds required to complete one full turn
SEC_PER_MOVE = 1  # Seconds required to move 10cm
MOTOR_DEFAULT_PWR = 30  # Default starting power for the motor
MOTOR_OFFSET_PWR = -1  # Difference between Motor 1 and Motor 2

# Define Position of sensors relative to robot frame (in cm)
# # [Sensor Name, Sensor Number, X location, Y location, Z location, Mask X, Mask Y, Mask Z]
# SENSOR_POS = [['HC-SR04', 1,    0,    8.5,  0, 0,  0,  0],
#               ['HC-SR04', 2, 7.36,   4.25,  0, 0, -1,  0],
#               ['HC-SR04', 3, 7.36,  -4.25,  0, 0,  1,  0],
#               ['HC-SR04', 4,    0,   -8.5,  0, 0, -1,  0],
#               ['HC-SR04', 5,-7.36,  -4.25,  0, 0,  1,  0],
#               ['HC-SR04', 6,-7.36,   4.25,  0, 0, -1,  0],
#               ['TSL2561', 1, 7.36,   4.25,  0, 0,  0, -1],
#               ['TSL2561', 2,    0,   -8.5,  0, 0,  0, -1],
#               ['TSL2561', 3,-7.36,   4.25,  0, 0,  0, -1]]

# Create sensor object
sensors = Sensor()

# Add sensors to sensor dictionary
sensors.addSensor('HC-SR04', 1, [    0,    8.5,  0,     math.pi/2])
sensors.addSensor('HC-SR04', 2, [ 7.36,   4.25,  0,     math.pi/6])
sensors.addSensor('HC-SR04', 3, [ 7.36,  -4.25,  0,    -math.pi/6])
sensors.addSensor('HC-SR04', 4, [    0,   -8.5,  0,    -math.pi/2])
sensors.addSensor('HC-SR04', 5, [-7.36,  -4.25,  0, -5*(math.pi/6)])
sensors.addSensor('HC-SR04', 6, [-7.36,   4.25,  0,  5*(math.pi/6)])
sensors.addSensor('TSL2561', 1, [    0,    8.5,  0, 0,     math.pi/6])
sensors.addSensor('TSL2561', 2, [    0,    8.5,  0, 0,    -math.pi/2])
sensors.addSensor('TSL2561', 3, [    0,    8.5,  0, 0,  5*(math.pi/6)])

# Define motor pins
Motor1A = 16  # Right Motor
Motor1B = 18
Motor1E = 22
Motor2A = 11  # Left Motor
Motor2B = 13
Motor2E = 15

# Define servo pins
Servo1 = 00 # Horizontal (Side to Side) servo
Servo2 = 00 # Vertical (Up and Down) servo


def main():

    print "Importing functions ..."

    from python_mysql_connect import connect, insert_current_pos, query_current_pos
    from motor import GPIOclean
    from maptool import pull_map
    from slam import slamfunc
    from kalmanfilter import kalman
    from navigation import navigate, explore

    print "Connecting to database ..."
    connect()

    print "Downloading map from database ..."
    pull_map()

    print "Starting main loop ..."

    for i in range(0, MAX_ITER):

        # Get current robot pose from database
        curr_pos = query_current_pos()

        # Move robot to new position based on current position and sensor input
        curr_input = navigate(curr_pos)

        # Explore (get dataset of points)
        scan = explore()

        # Use current position and explore dataset to determine new location
        #curr_pos_slam = slamfunc(scan, curr_pos)

        # Feed SLAM estimate of position into Kalman Filter
        # curr_pos_filter = kalman(curr_pos, curr_pos_slam, curr_input)
        curr_pos_filter = kalman(curr_pos, curr_pos, curr_input)

        # print curr_pos # Last known filtered state of robot
        # print curr_meas # Current approximate state of robot
        # print curr_input # Input vector which was inputed since last known state
        # print curr_pos_filter # New filtered state of robot

        # Push new robot pose to database
        insert_current_pos(curr_pos_filter)

    print "Exited main loop ..."

    print "Pushing map to database ..."
    push_map()

    print "Clean up motor GPIO ..."
    GPIOclean()


if __name__ == '__main__':
    main()
