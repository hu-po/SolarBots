# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room

import numpy as np
import numpy.linalg as la
from brain import params, sensors
# from python_mysql_connect import insert_sensor_data, insert_current_pos, query_current_pos


def vector_angle(v1, v2):
    '''
        Returns angle in radians between vectors 'v1' and 'v2'
    '''
    cosang = np.dot(v1, v2)
    sinang = la.norm(np.cross(v1, v2))
    return np.arctan2(sinang, cosang)


class Move:

    def __init__(self):

        # Type of move
        # - Virtual: move was performed virtually to connect nodes in the graph
        # - Real: move was performed by the robot and has sensor data to prove it
        self.type = None

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
        self.global_pos_vectors = []
        self.weighted_pos_vectors = []

    def getMotionPlan(self):
        '''
            Breaks a move (self object) down into motion primitives to be executed by motor
            functions
        '''

    # Get angle difference between desired movement vector and generic
    # "forward vector"
        self.rot_angle = vector_angle(
            params.p['FORWARD_VECTOR'], self.direction_vector)

        # Get forward motion from desired movement vector
        self.distance = params.p['MOVE_PER_TURN'] * self.direction_vector

        # Set movement delta list (delX, delY, delZ, delTheta)
        self.delta = self.distance.tolist()
        self.delta.append(self.rot_angle)

        # Determine direction of rotation
        if self.rot_angle < 0:
            self.primitives.append(('left', abs(self.rot_angle)))

        if self.rot_angle > 0:
            self.primitives.append(('right', abs(self.rot_angle)))

        # Determine direction of movement
        # TODO: eventually return 'backwards' if the angle rotation required is
        # smaller
        self.primitives.append(('forward', la.norm(self.distance)))

    def push_to_database(self, smooth_data):
        '''
            Push move information (along with reading) to the database
        '''

        # TODO: print this to mysql
        print "Push to database..."

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

    def describe(self):
        '''
            Prints out information about the move
        '''

        print "Move description: "
        print "          TYPE: " + str(self.type)
        print "   INITIAL POS: " + str(self.initial_pos)
        print "     FINAL POS: " + str(self.final_pos)
        print " DIRECTION VEC: " + str(self.direction_vector)
        print "    PRIMITIVES: " + str(self.primitives)
        print "         DELTA: " + str(self.delta)
        print "      RAW DATA: " + str(self.raw_data)
        print "   SMOOTH DATA: " + str(self.smooth_data)
        print "    POS VECTOR: " + str(self.pos_vectors)
        print "GLOBAL POS VEC: " + str(self.global_pos_vectors)
        print "WEIGHT POS VEC: " + str(self.weighted_pos_vectors)