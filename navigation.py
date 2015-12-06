# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program takes in current position, and uses the map to
# determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from motor import moveBot
from Move import Move
from Area import Area
from Buzzer import Buzzer
import time
# import camera
# from kalmanfilter import kalman

import numpy as np
import numpy.linalg as la

# Moves to exsisting area, returns area object
def navigate(room, new_area):

    # initialize room.current_area if it does not exsist
    if not room.current_area:
        room.current_area = Area()

    # Test output
    print "Navigating (moving to a known area) ..."

    # Beep to indicate begining of navigate step
    buzzer = Buzzer()
    buzzer.play(4)

    # Make sure a path exsists between the two areas
    if room.current_area not in new_area.previous:
        print "No path between nodes"
        return

    # Get move required to travel between areas
    move = new_area.moves_performed[room.current_area.name]

    # TODO: moves_performed will just be the latest move performed between the two areas
    # Need to find a way to find the "best" move between them

    # Execute motion primitives between nodes
    for (direction, amount) in move.primitives:
        print "Moving" + str(direction) + " " + str(amount)
        # moveBot(direction, amount, params.p['MOTOR_PWR'])

    # Get final position by summing initial position and delta
    move.final_pos = [init + delt for init, delt in zip(move.initial_pos, move.delta)]

    # TODO: put a kalman filter on the movement. Use camera and sonar as
    # truth? Not sure here

    # TODO: figure out what area you are in by looking at pictures
    new_area.localize

    # Add move to new area's dictionary of moves
    new_area.moves_performed[room.current_area.name] = move

def explore(room):  # Move to a new area, returns area object

    # initialize room.current_area if it does not exsist
    if not room.current_area:
        room.current_area = Area()

    # Test output
    print "Exploring (moving to a new location) ..."

    # Beep to indicate begining of explore step
    buzzer = Buzzer()
    buzzer.play(5)

    # Create new area and move objects
    new_area = Area()
    move = Move()

    # Make sure move is set as a real move (performed by robot)
    move.type = "Real"

    # Link it to the previous object
    new_area.previous.append(room.current_area.name)

    # Initial position set to position of previous area
    move.initial_pos = room.current_area.pos

    # Vector of movement used
    move = get_move_vector(move)

    # Break down movement vector into motion primitives that robot can execute
    move.getMotionPlan()

    for (direction, amount) in move.primitives:
        print "Moving " + str(direction) + " " + str(amount)
        # moveBot(direction, amount, params.p['MOTOR_PWR'])

    # Get final position by summing initial position and delta
    move.final_pos = [init + delt for init, delt in zip(move.initial_pos, move.delta)]

    # TODO: put a kalman filter on the movement. Use camera and sonar as
    # truth? Not sure here

    # # Test print
    # print "Describing move in explore function"
    move.describe()

    # Update location of new area to final position of move
    new_area.pos = move.final_pos

    # Add move to new area's dictionary of moves
    new_area.moves_performed[room.current_area.name] = move

    # Redirect current area to this new_area
    room.current_area = new_area

    # Localize bot in new area
    # new_area.localize

    # # Test print
    # print "Describing new_area in explore function"
    # new_area.describe()

    # Append new_area to room
    room.areas.append(new_area)

    # Return updated room object
    return room

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

    # Simple median smoothing
    for i in range(len(data[0])):

        # Make a list of all the different readings from one
        strip = [sample[i] for sample in data]

        # Add them to data_smooth
        data_smooth.append(np.median(np.array(strip)))

        # print i
        # print data_smooth[i]

    return data_smooth


# Performs movement based on gradient direction of sensor readings.
# Returns vector direction of movement
def get_move_vector(move):

    # Read in raw data from sensors
    move.raw_data = readData()

    # Smooth raw data from sensors
    move.smooth_data = smoothData(move.raw_data)

    # Determine position vectors for sensor data (with respect to robot frame)
    move.pos_vectors = [sensors.to_robot(sensors.sensor_names[i], move.smooth_data[i])
                        for i in range(len(sensors.sensor_names))]

    # Determine position vectors for sensor data (with respect to global frame)
    move.global_pos_vectors = [sensors.to_global(sensors.sensor_names[i], move.smooth_data[i], move.initial_pos)
                        for i in range(len(sensors.sensor_names))]

    # Combine readings together using sensor weights
    for i in range(len(move.pos_vectors)):
        # Second element in sensor dictionary entry is sensor weight
        sensor_weight = sensors.s[sensors.sensor_names[i]][1]
        # Multiply pos readings by sensor weight
        weighted_vector = np.multiply(
            sensor_weight, move.pos_vectors[i]).tolist()
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
