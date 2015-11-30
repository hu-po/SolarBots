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


# Returns the angle in radians between vectors 'v1' and 'v2'
def vector_angle(v1, v2):
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

# Breaks a move down into motion primitives to be executed by motor functions


def getMotionPlan(move):

    # Get angle difference between desired movement vector and generic
    # "forward vector"
    move.rot_angle = vector_angle(
        params.p['FORWARD_VECTOR'], move.direction_vector)

    # Get forward motion from desired movement vector
    move.distance = params.p['MOVE_PER_TURN'] * move.direction_vector

    # Set movement delta list (delX, delY, delZ, delTheta)
    move.delta = move.distance.tolist()
    move.delta.append(move.rot_angle)

    # Determine direction of rotation
    if move.rot_angle < 0:
        move.primitives.append(('left', abs(move.rot_angle)))

    if move.rot_angle > 0:
        move.primitives.append(('right', abs(move.rot_angle)))

    # Determine direction of movement
    # TODO: eventually return 'backwards' if the angle rotation required is
    # smaller
    move.primitives.append(('forward', la.norm(move.distance)))

    # Return updated move object
    return move


# Moves to exsisting area, returns area object
def navigate(old_area, new_area):

    # Beep to indicate begining of navigate step
    buzzer = Buzzer()
    buzzer.play(4)

    # TODO: Travel from old area to an already exsisting area, breaking down
    # movement into primitives

    return area_traveled_to


def explore(old_area=None):  # Move to a new area, returns area object

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
    move = get_move_vector(move)

    # Break down movement vector into motion primitives that robot can execute
    move = getMotionPlan(move)

    for (direction, amount) in move.primitives:
        print "Moving" + str(direction) + " " + str(amount)
        # moveBot(direction, amount, params.p['MOTOR_PWR'])

    # Get final position by summing initial position and delta
    move.final_pos = [init + delt for init, delt in zip(move.initial_pos, move.delta)]

    # TODO: put a kalman filter on the movement. Use camera and sonar as
    # truth? Not sure here

    # Add move to new area's dictionary of moves
    new_area.moves_performed.append(move)

    # Take pictures and add to dictionary of pictures
    # new_area.pics = camera.takePics()

    # Return current area
    return new_area


def sample():  # Sample the Arduino sensors
    print "inside sample()"

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

    # Testing prints
    # print "raw_data inside get_move_vector:"
    # print move.raw_data
    # print "smooth_data inside get_move_vector:"
    # print move.smooth_data
    # print "pos_vectors inside get_move_vector:"
    # print move.pos_vectors
    # print "weighted_pos_vectors inside get_move_vector:"
    # print move.weighted_pos_vectors
    # print "direction_vector inside get_move_vector:"
    # print move.direction_vector

    # Return move object
    return move


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
