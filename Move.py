# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room

import numpy as np
import numpy.linalg as la
from brain import params, sensors

def vector_angle(v1, v2):
    '''
        Returns angle in radians between vectors 'v1' and 'v2'
    '''
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)


class Move:

    def __init__(self):

        # Initial position [X, Y, Z, Theta]
        self.initial_pos = [0, 0, 0, 0]

        # Calculated final position [X, Y, Z, Theta]
        self.final_pos = [0, 0, 0, 0]

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
        self.raw_data = []
        self.smooth_data = []
        self.pos_vectors = []
        self.weighted_pos_vectors = []

    def getMotionPlan(self):
        '''
            Breaks a move (self object) down into motion primitives to be executed by motor
            functions
        '''

        # Determine motion primitives based on direction vector
        # if self.direction_vector[0] > 0 and self.direction_vector[1] > 0:
        ref_vector = params.p['FORWARD_VECTOR']
        rot_direction = 'right'
        move_direction = 'forward'

        if self.direction_vector[0] < 0 and self.direction_vector[1] > 0:
            # print "Rotating left and then forward"
            ref_vector = params.p['FORWARD_VECTOR']
            rot_direction = 'left'
            move_direction = 'forward'

        if self.direction_vector[0] > 0 and self.direction_vector[1] < 0:
            # print "Rotating left and then backward"
            ref_vector = params.p['BACKWARD_VECTOR']
            rot_direction = 'left'
            move_direction = 'backward'

        if self.direction_vector[0] < 0 and self.direction_vector[1] < 0:
            # print "Rotating right and then backward"
            ref_vector = params.p['BACKWARD_VECTOR']
            rot_direction = 'right'
            move_direction = 'backward'

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

    def describe(self):
        '''
            Prints out information about the move
        '''

        print "Move description: "
        print "   INITIAL POS: " + str(self.initial_pos)
        print "     FINAL POS: " + str(self.final_pos)
        print " DIRECTION VEC: " + str(self.direction_vector)
        print "    PRIMITIVES: " + str(self.primitives)
        print "         DELTA: " + str(self.delta)
        print "      RAW DATA: " + str(self.raw_data)
        print "   SMOOTH DATA: " + str(self.smooth_data)
        print "    POS VECTOR: " + str(self.pos_vectors)
        print "WEIGHT POS VEC: " + str(self.weighted_pos_vectors)