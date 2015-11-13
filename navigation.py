# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program takes in current position, and uses the map to
# determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from motor import moveBot
import numpy as np
import datetime
import maptool
from python_mysql_connect import insert_sensor_data, insert_current_pos, query_current_pos


def navigate(curr_pos):
    # given a position? find somewhere to move which makes sense?
    # Somehow break these down into motion primitives?

    # Perform exploration movement
    moveBot('forward', 1, params.p('MOTOR_PWR'))  # Move forward 1 unit (10 cm)

    curr_input = np.array([10, 0, params.p('EXPLORE_ANGLE')]).reshape(-1, 1)

    return curr_input


def sample():

    points = []
    points = filter('', points)
    while len(points) != 6:
        points = ser.readline().strip().split(',')
        # print points
        # print len(points)
        # print "garbage"
    return points


def readData():
    print "Reading data ..."

    # Create empty data array to store data
    data = np.empty([params.p('DATA_SAMPLE_SIZE'), (sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'))])

    # Populate empty data array
    for i in range(0, params.p('DATA_SAMPLE_SIZE')):

        # print data(i,:)
        data[i, :] = sample()

    return data


def smoothData(data):

    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = np.empty([sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'), 1])

    # Simple median smoothing
    for i in range(0, sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561')):
        # print i
        # print data_smooth[i]
        # print data[:, i]
        # print np.median(data[:, i])
        data_smooth[i] = np.median(data[:, i])

    # TODO: More ridiculous smoothing

    return data_smooth


def explore():
    print "Exploring current location ..."

    # Initialize exploration results matrix
    explore_results = np.empty([sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'), params.p('EXPLORE_ITER')])

    print explore_results

    for i in range(0, params.p('EXPLORE_ITER')):

        # Read in raw data from sensors
        raw_data = readData()

        # Smooth raw data from sensors
        smooth_data = smoothData(raw_data)

        #print raw_data
        #print smooth_data

        smooth_data = smooth_data.tolist()

        # Write data to MySQL
        for j in range(0, sensors.numSensor('HC-SR04')):
            # HC-SR04 Sensor
            # print 'HC-SR04'
            # print j
            # print smooth_data[j]
            # print datetime.datetime.now()
            insert_sensor_data(('HC-SR04', j + 1, smooth_data[j][0], datetime.datetime.now()))

        for j in range(0, sensors.numSensor('TSL2561')):
            # TSL2561 Sensor
            # print 'TSL2561'
            # print NUM_SONAR + j
            # print smooth_data[NUM_SONAR + j]
            # print datetime.datetime.now()
            insert_sensor_data(('TSL2561', j + 1, smooth_data[sensors.numSensor('HC-SR04') + j][0], datetime.datetime.now()))

        print explore_results[:, i]

        # Store smooth data in exploration results matrix
        explore_results[:, i] = np.array(smooth_data).flatten()

        # Rotate robot to get another set of data
        # Ultimately make a 360 degree turn during exploration
        moveBot('turnleft', (params.p('EXPLORE_ANGLE') / params.p('EXPLORE_ITER')), params.p('MOTOR_PWR'))

    return explore_results


def main():
    explore()

if __name__ == '__main__':
    main()
