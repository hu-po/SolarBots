# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Definitions for all parameters, runs/calls all other functions

import serial
import numpy as np
import datetime
from python_mysql_connect import connect, insert_current_pos, query_current_pos
from motor import clean
from maptool import update_map
from slam import slamfunc
from kalmanfilter import kalman
from navigation import navigate, explore

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Define Navigation Parameters
DATA_SAMPLE_SIZE = 3   # Sample size for data (increase to stabilize at cost of speed)
NUM_SONAR = 3  # Number of sonar sensors
NUM_LIGHT = 3   # Number of light sensors
MAX_ITER = 10   # Maximum number of Sense-Plan-Act Cycles
MOTOR_PWR = 30  # 0 - 100 speed of motor
EXPLORE_ITER = 4  # Number of sensor readings in an explore scan
EXPLORE_ANGLE = 360.0 # Angle to explore during an explore scan

# Define SLAM Parameters (distance/angle perturbations)
FOG_RADIUS = 100  # Radius of section of map to use (centered around current position) for SLAM
RAND_DIST_MU = 0 # Center of distribution (cm)
RAND_DIST_SIGMA = 1 # Standard deviation (cm)
RAND_ANG_MU = 0 # Degrees
RAND_ANG_SIGMA = 10 # Degrees
RAND_NUM = 10 # Number of random samples

# Define Kalman Filter Parameters
OBSERVATION_NOISE = 0.1

# Define Motor Parameters
SEC_PER_TURN = 10   # Seconds required to complete one full turn
SEC_PER_MOVE = 1  # Seconds required to move 10cm
MOTOR_DEFAULT_PWR = 30  # Default starting power for the motor
MOTOR_OFFSET_PWR = -1  # Difference between Motor 1 and Motor 2

# Define Position of sensors relative to robot frame (in cm)
TSL2561_1_x = - 8.23
TSL2561_1_y = 4.75
TSL2561_2_x = 8.23
TSL2561_2_y = 4.75
TSL2561_3_x = 0
TSL2561_3_y = - 9.5
HCSR04_1_x = 0
HCSR04_1_y = 6
HCSR04_2_x = 9.5
HCSR04_2_y = 0
HCSR04_3_x = - 9.5
HCSR04_3_y = 0

# Define motor pins
Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 15
Motor2B = 13
Motor2E = 11

def main():

    print "Connecting to database ..."
    connect()

    print "Downloading latest map from database ..."
    # update_map()

    print "Starting main loop ..."

    for i in range(0, MAX_ITER):

        # Get current robot pose from database
        curr_pos = query_current_pos()

        # Move robot to new position based on current position and sensor input
        curr_input = navigate(curr_pos)

        # Explore (get dataset of points)
        scan = explore()

        # Use current position and explore dataset to determine new location
        curr_pos_slam = slamfunc(scan, curr_pos)

        # Feed SLAM estimate of position into Kalman Filter
        curr_pos_filter = kalman(curr_pos, curr_meas=curr_pos_slam, curr_input)

        # print curr_pos # Last known filtered state of robot
        # print curr_meas # Current approximate state of robot
        # print curr_input # Input vector which was inputed since last known state
        # print curr_pos_filter # New filtered state of robot

        # Push new robot pose to database
        insert_current_pos(curr_pos)

    print "Exited main loop ..."

    print "Clean up motor GPIO ..."
    GPIOclean()

if __name__ == '__main__':
    main()
