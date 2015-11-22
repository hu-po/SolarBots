# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program takes in current position, and uses the map to
# determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from actions import moveBot, beep
import Move
import Area

import numpy as np
import datetime
import maptool
from python_mysql_connect import insert_sensor_data, insert_current_pos, query_current_pos


def navigate(old_area, des_area):

    # TODO: Travel from old area to new area, break down movement into primitives

    return


def explore(old_area): # Move to a new area

    # Test output
    print "Exploring (moving to a new location) ..."
    beep()

    # Create new area and move objects
    new_area = Area()
    move = Move()

    # Link it to the previous object
    new_area.previous = old_area

    # Initial position set to position of previous area
    move.initial_pos = origin_area.pos

    # Vector of movement used
    move.move_vector = get_move_vector()

    # TODO: Perform movement based on vector direction
    #   - break down into motion primitives, rounding as necessary
    #   - perform motion primitives using moveBot. (forward/backwards with some amount and left/right with some amount)

    for (direction, amount) in primitives:
        moveBot(direction, amount, params.p('MOTOR_PWR'))
        # EXAMPLE CALL: moveBot('forward', 1, params.p('MOTOR_PWR'))  # Move
        # forward 1 unit (10 cm)

        # Rotation performed / Distance traveled
        if direction in ['left', 'right']:
            move.rot_angle = amount
        if direction in ['forward', 'backward']:
            move.distance = amount

    # Calculated final position
    move.final_pos = move.initial_pos + np.concatenate(move.distance, move.rot_angle) # TODO: Proper function call to concatenate

    # Add move to new area's dictionary of moves
    new_area.moves_performed.append(move)

    # Take pictures and add to dictionary of pictures
    # TODO: Get Pictures (ideally some sort of panorama shot)
    new_area.pics = {}

def sample():  # Sample the Arduino sensors

    points = []
    points = filter('', points)
    while len(points) != sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'):
        points = ser.readline().strip().split(',')
        # print points
        # print len(points)
        # print "garbage"
    return points


def readData():
    print "Reading data ..."

    # Create empty data array to store data
    data = np.empty([params.p('DATA_SAMPLE_SIZE'), (sensors.numSensor(
        'HC-SR04') + sensors.numSensor('TSL2561'))])

    # Populate empty data array
    for i in range(0, params.p('DATA_SAMPLE_SIZE')):

        # print data(i,:)
        data[i, :] = sample()

    return data


def smoothData(data):

    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = np.empty(
        [sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'), 1])

    # Simple median smoothing
    for i in range(0, sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561')):
        # print i
        # print data_smooth[i]
        # print data[:, i]
        # print np.median(data[:, i])
        data_smooth[i] = np.median(data[:, i])

    # TODO: More ridiculous smoothing

    return data_smooth.tolist()


# Performs movement based on gradient direction of sensor readings.
# Returns vector direction of movement
def get_move_vector():

    # Read in raw data from sensors
    raw_data = readData()

    # Smooth raw data from sensors
    smooth_data = smoothData(raw_data)

    # Determine position vectors for sensor data (with respect to robot frame)
    pos_vectors = [
        sensors.to_robot(sensor_key, smooth_data) for sensor_key in sensors.s]

    # Combine readings together, using weights, to determine ultimate
    # vector_direction of travel
    # TODO: Check whether this is the proper axis for this
    direction_vector = np.mean(sensors.apply_weights(pos_vectors), axis=1)

    return direction_vector


def main():
    explore()

if __name__ == '__main__':
    main()

# --------------------- OLD CODE
# def explore():
#     print "Exploring current location ..."

# Initialize exploration results matrix
#     explore_results = np.empty([sensors.numSensor('HC-SR04') + sensors.numSensor('TSL2561'), params.p('EXPLORE_ITER')])

#     print explore_results

#     for i in range(0, params.p('EXPLORE_ITER')):

# Read in raw data from sensors
#         raw_data = readData()

# Smooth raw data from sensors
#         smooth_data = smoothData(raw_data)

# print raw_data
# print smooth_data

#         smooth_data = smooth_data.tolist()

# Write data to MySQL
#         for j in range(0, sensors.numSensor('HC-SR04')):
# HC-SR04 Sensor
# print 'HC-SR04'
# print j
# print smooth_data[j]
# print datetime.datetime.now()
#             insert_sensor_data(('HC-SR04', j + 1, smooth_data[j][0], datetime.datetime.now()))

#         for j in range(0, sensors.numSensor('TSL2561')):
# TSL2561 Sensor
# print 'TSL2561'
# print NUM_SONAR + j
# print smooth_data[NUM_SONAR + j]
# print datetime.datetime.now()
#             insert_sensor_data(('TSL2561', j + 1, smooth_data[sensors.numSensor('HC-SR04') + j][0], datetime.datetime.now()))

#         print explore_results[:, i]

# Store smooth data in exploration results matrix
#         explore_results[:, i] = np.array(smooth_data).flatten()

# Rotate robot to get another set of data
# Ultimately make a 360 degree turn during exploration
#         moveBot('turnleft', (params.p('EXPLORE_ANGLE') / params.p('EXPLORE_ITER')), params.p('MOTOR_PWR'))

#     return explore_results
