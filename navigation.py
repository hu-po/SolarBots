# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program takes in current position, and uses the map to
# determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from motor import moveBot
from Move import Move
from Area import Area
from Buzzer import Buzzer
# import camera

import numpy as np
import datetime

# Moves to exsisting area, returns area object
def navigate(old_area, new_area):

    # Beep to indicate begining of navigate step
    buzzer = Buzzer()
    buzzer.play(4)

    # TODO: Travel from old area to an already exsisting area, breaking down
    # movement into primitives

    return area_traveled_to


def explore(old_area):  # Move to a new area, returns area object

    # Set old_area to None if this is first pass
    if not old_area:
        old_area = Area()

    # Test output
    print "Exploring (moving to a new location) ..."

    # Beep to indicate begining of explore step
    buzzer = Buzzer()
    buzzer.play(5)

    # Create new area and move objects
    new_area = Area()
    move = Move()

    # Link it to the previous object
    new_area.previous = old_area

    # Initial position set to position of previous area
    move.initial_pos = old_area.pos

    # Vector of movement used
    move.move_vector = get_move_vector()

    # TODO: Perform movement based on vector direction
    #   - break down into motion primitives, rounding as necessary
    #   - perform motion primitives using moveBot. (forward/backwards with some amount and left/right with some amount)

    for (direction, amount) in primitives:
        moveBot(direction, amount, params.p['MOTOR_PWR'])
        # EXAMPLE CALL: moveBot('forward', 1, params.p['MOTOR_PWR'])  # Move
        # forward 1 unit (10 cm)

        # Rotation performed / Distance traveled
        if direction in ['left', 'right']:
            move.rot_angle = amount
        if direction in ['forward', 'backward']:
            move.distance = amount

    # Calculated final position
    # TODO: Proper function call to concatenate
    move.final_pos = move.initial_pos + \
        np.concatenate(move.distance, move.rot_angle)

    # Add move to new area's dictionary of moves
    new_area.moves_performed.append(move)

    # Take pictures and add to dictionary of pictures
    # new_area.pics = camera.takePics()

    # Return current area
    return new_area


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
    data = np.empty([params.p['DATA_SAMPLE_SIZE'], (sensors.numSensor(
        'HC-SR04') + sensors.numSensor('TSL2561'))])

    # Populate empty data array
    for i in range(0, params.p['DATA_SAMPLE_SIZE']):

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

    # Testing prints
    print "raw_data inside get_move_vector:"
    print raw_data
    print "smooth_data inside get_move_vector:"
    print smooth_data

    # Determine position vectors for sensor data (with respect to robot frame)
    pos_vectors = [
        sensors.to_robot(sensor_key, smooth_data) for sensor_key in sensors.s]

    print "pos_vectors inside get_move_vector:"
    print pos_vectors

    # Combine readings together using sensor weights
    weighted_pos_vectors = np.multiply(
        sensors.get_weights(), pos_vectors)  # TODO: Do this properly

    print "weighted_pos_vectors inside get_move_vector:"
    print weighted_pos_vectors

    # Combine weighted position vectors to get ultimate direction vector
    # TODO: Check whether this is the proper axis for this
    direction_vector = np.mean(weighted_pos_vectors, axis=1)

    print "direction_vector inside get_move_vector:"
    print direction_vector

    return direction_vector


def main():
    explore(None)

if __name__ == '__main__':
    main()

# --------------------- OLD CODE
# def explore():
#     print "Exploring current location ..."

# Initialize exploration results matrix
# explore_results = np.empty([sensors.numSensor('HC-SR04') +
# sensors.numSensor('TSL2561'), params.p['EXPLORE_ITER')])

#     print explore_results

#     for i in range(0, params.p['EXPLORE_ITER')):

# Read in raw data from sensors
#         raw_data = readData()

# Smooth raw data from sensors
#         smooth_data = smoothData(raw_data)

# print raw_data
# print smooth_data

#         smooth_data = smooth_data.tolist()


#         print explore_results[:, i]

# Store smooth data in exploration results matrix
#         explore_results[:, i] = np.array(smooth_data).flatten()

# Rotate robot to get another set of data
# Ultimately make a 360 degree turn during exploration
# moveBot('turnleft', (params.p['EXPLORE_ANGLE') /
# params.p['EXPLORE_ITER')), params.p['MOTOR_PWR'))

#     return explore_results
