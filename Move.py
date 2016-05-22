# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room

from __future__ import print_function
import numpy as np
import numpy.linalg as la
from brain import params, sensors

# Directional constants
FORWARD = "forward"
BACKWARD = "backward"
LEFT = "left"
RIGHT = "right"

def vector_angle(v1, v2):
    '''
        Returns angle in radians between vectors 'v1' and 'v2'
    '''
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)

def sample():
    '''
        Sample Arduino sensors and return datapoints
    '''
    # Set timeout time (0.1 seconds)
    timeout = time.time() + params.p['TIMEOUT']

    # Initialize points list and begin loop
    points = []
    while len(points) != sensors.numSensor(['HC-SR04', 'TSL2561']):

        # Gather points from serial object
        points = ser.readline().strip().split(',')

        # If function times out, set points to empty array and break
        if time.time() > timeout:
            points = [0] * (sensors.numSensor(['HC-SR04', 'TSL2561']))
            break

    return points

def smoothData(data):

    # Create empty data array to store smooth data
    data_smooth = []

    # # Test print
    # print("Data: ", data)

    # Simple median smoothing
    for i in xrange(len(data[0])):

        # Make a list of all the different readings from one
        strip = [int(sample[i]) for sample in data]
        # TODO: see why this int is there

        # Add them to data_smooth
        data_smooth.append(np.median(strip))

    return data_smooth

class MoveException(Exception):
    pass

class Move(object):

    def __init__(self):

        # Vector of movement used
        self.direction_vector = []

        # Rotation performed
        self.rot_angle = []

        # Distance traveled
        self.distance = []

        # Motion primitives to perform move
        self.primitives = []

        # Motion delta (delX, delY, delZ, delTheta)
        self.delta = [0, 0, 0, 0]

        # Sensor data for the move (populated in navigation.get_move_vector)
        self.smooth_data = []
        self.weighted_pos_vectors = []

    def get_motion_plan(self):
        '''
            Breaks a move (self object) down into motion primitives to be executed by motor
            functions
        '''

        try:
            # Determine motion primitives based on direction vector
            if self.direction_vector[0] > 0 and self.direction_vector[1] > 0:
                # print("Rotating right and then moving forward")
                ref_vector = params.p['FORWARD_VECTOR']
                rot_direction = RIGHT
                move_direction = FORWARD
            elif self.direction_vector[0] < 0 and self.direction_vector[1] > 0:
                # print("Rotating left and then moving forward")
                ref_vector = params.p['FORWARD_VECTOR']
                rot_direction = LEFT
                move_direction = FORWARD
            elif self.direction_vector[0] > 0 and self.direction_vector[1] < 0:
                # print("Rotating left and then moving backward")
                ref_vector = params.p['BACKWARD_VECTOR']
                rot_direction = LEFT
                move_direction = BACKWARD
            elif self.direction_vector[0] < 0 and self.direction_vector[1] < 0:
                # print("Rotating right and then moving backward")
                ref_vector = params.p['BACKWARD_VECTOR']
                rot_direction = RIGHT
                move_direction = BACKWARD
            else:
                raise MoveException("Move object cannot get motion plan without a direction vector")
        except MoveException:
            return # Exit if function is called with incomplete data


        # Get angle difference between desired movement vector and previously defined reference vector
        self.rot_angle = vector_angle(self.direction_vector, ref_vector)

        # Get motion from desired movement vector
        self.distance = params.p['MOVEMENT_WEIGHT'] * self.direction_vector

        # Set movement delta list (delX, delY, delZ, delTheta)
        self.delta = self.distance.tolist()
        self.delta.append(self.rot_angle)

        # Add motion primitives to move object (rotation then translation)
        self.primitives.append((rot_direction, abs(self.rot_angle)))
        self.primitives.append((move_direction, la.norm(self.distance)))

    def get_move_vector(self):
        '''
            Performs movement based on gradient direction of sensor readings.
            Returns vector direction of movement
        '''

        # Read and Smooth raw data from sensors
        raw_data = (sample() for i in xrange(params.p['DATA_SAMPLE_SIZE']))
        self.smooth_data = smoothData(raw_data)

        # Combine readings together using sensor weights
        for data, sensr in zip(self.smooth_data, sensors.s.iterkeys()):

            # Determine position vector for sensor data (with respect to robot frame)
            pos_vector = sensors.to_robot(sensr, data)

            # Second element in sensor dictionary entry is sensor weight
            sensor_weight = sensors.s[sensr][1]

            # Multiply pos readings by sensor weight
            weighted_vector = np.multiply(sensor_weight, pos_vector).tolist()

            self.weighted_pos_vectors.append(weighted_vector)

            # Debug print statements
            # print("sensr, ", sensr)
            # print("data, ", data)
            # print("pos_vector, ", pos_vector)
            # print("sensor_weight, ", sensor_weight)
            # print("weighted_vector, ", weighted_vector)

        # Combine weighted position vectors to get ultimate direction vector
        self.direction_vector = np.mean(np.array(self.weighted_pos_vectors), axis=0)

    def __str__(self):
        '''
            Prints out information about the move
        '''

        return "Move object description:  \n DIRECTION VEC: {}\n    PRIMITIVES: {}\n         DELTA: {}\n   SMOOTH DATA: {}\nWEIGHT POS VEC: {}" \
            .format(
             str(self.direction_vector),
             str(self.primitives),
             str(self.delta),
             str(self.smooth_data),
             str(self.weighted_pos_vectors))