# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program uses the sensors to determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from motor import moveBot
from Buzzer import Buzzer
from Move import Move
import time

import numpy as np
import numpy.linalg as la

def navigate():
    '''
        Function will call exploration() function to move robot, but will keep
        track of previous moves
    '''

    # Test output
    print "Navigating ..."

    # Beep to indicate begining of navigate step
    buzzer = Buzzer()
    buzzer.play(4)

    # Initialize list for history of moves, start it with a "blank" move
    move_hist = [Move()]

    # Enter the exploration loop
    for i in range(params.p['MAX_ITER']):

        # Execute explore function and save results
        move_hist.append(explore(move_hist[-1]))

        # Wait between moves
        time.sleep(params.p['WAIT_TIME'])

def explore(old_move):
    '''
        Function will initialize and execute a new "move"
        In: previous move
        Out: new move
    '''

    # Test output
    print "Exploring (moving to a new location) ..."

    # Beep to indicate begining of explore step
    buzzer = Buzzer()
    buzzer.play(5)

    # Initialize new move object
    move = Move()

    # Initial position set to position of previous area
    move.initial_pos = old_move.final_pos

    # Vector of movement used
    move = get_move_vector(move)

    # Break down movement vector into motion primitives that robot can execute
    move.getMotionPlan()

    # Get final position by summing initial position and delta
    move.final_pos = [init + delt for init, delt in zip(move.initial_pos, move.delta)]

    # Debug print move fields
    move.describe()

    # Execute motion from given move primitives
    for (direction, amount) in move.primitives:
        print "Moving " + str(direction) + " " + str(amount)
        moveBot(direction, distance=amount, num=params.p['MOTOR_PWR'])

    # Return finished move object
    return move

def sample():
    '''
        Sample Arduino sensors and return datapoints
    '''
    # Set timeout time (2 seconds)
    timeout = time.time() + params.p['TIMEOUT']

    # Initialize points list and begin loop
    points = []
    while len(points) != sensors.numSensor(['HC-SR04', 'TSL2561']):
        points = ser.readline().strip().split(',')

        # If function times out, set points to empty array and break
        if time.time() > timeout:
            points = [0] * (sensors.numSensor(['HC-SR04', 'TSL2561']))
            break

    return points


def readData():
    print "Reading data ..."

    # Create empty data list to store data
    data = []

    # Populate empty data array
    for i in range(params.p['DATA_SAMPLE_SIZE']):
        data.append(sample())

    return data


def smoothData(data):
    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = []

    # # Test print
    # print "Data: ", data

    # Simple median smoothing
    for i in range(len(data[0])):

        # Make a list of all the different readings from one
        strip = [sample[i] for sample in data]

        # print "Strip: ", strip

        # Add them to data_smooth
        data_smooth.append(np.median(map(int, strip)))

    return data_smooth


def get_move_vector(move):
    '''
        Performs movement based on gradient direction of sensor readings.
        Returns vector direction of movement
    '''

    # Read in raw data from sensors
    move.raw_data = readData()

    # Smooth raw data from sensors
    move.smooth_data = smoothData(move.raw_data)

    # Determine position vectors for sensor data (with respect to robot frame)
    move.pos_vectors = [sensors.to_robot(sensors.sensor_names[i], move.smooth_data[i])
                        for i in range(len(sensors.sensor_names))]

    # Combine readings together using sensor weights
    for i in range(len(move.pos_vectors)):
        # Second element in sensor dictionary entry is sensor weight
        sensor_weight = sensors.s[sensors.sensor_names[i]][1]
        # Multiply pos readings by sensor weight
        weighted_vector = np.multiply(sensor_weight, move.pos_vectors[i]).tolist()

        move.weighted_pos_vectors.append(
            [item for sublist in weighted_vector for item in sublist])  # Flatten result

    # Combine weighted position vectors to get ultimate direction vector
    move.direction_vector = np.mean(
        np.array(move.weighted_pos_vectors), axis=0)

    # Return move object
    return move

def main():
    explore(None)

if __name__ == '__main__':
    main()
