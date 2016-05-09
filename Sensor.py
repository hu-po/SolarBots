# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Sensor class defines sensor objects, with location, type,
#               as well as frame transformation functions etc

import numpy as np
from numpy import cos, sin
import logging

def calculateTransform(loc):
    '''
        Calculates the 4x4 transform to a frame
    '''
    # Transformation for 3D Rotation along Z-Axis by Theta
    rotation = [[cos(loc[3]), -sin(loc[3]),  0,  0],
                [sin(loc[3]),  cos(loc[3]),  0,  0],
                [0,            0,  1,  0],
                [0,            0,  0,  1]]

    # Transformation for 3D Translation along X and Y Axis
    translation = [[1, 0, 0,  loc[0]],
                   [0, 1, 0,  loc[1]],
                   [0, 0, 1,  loc[2]],
                   [0, 0, 0,       1]]

    T = np.dot(translation, rotation)

    # Return transform
    return T


class Sensor(object):

    def __init__(self):

        # Initialize sensor dictionary
        self.s = {}

        # Initialize list of sensor names
        self.sensor_names = []

    def addSensor(self, name, num, weight, location):
        '''
            Adds a sensor (+info) to the dictionary within the Sensor object
        '''

        # Name, number, location (in robot frame), and transformation (to robot
        # frame) of sensor
        self.s[(name, num)] = (location, weight, calculateTransform(location))

        # Add sensor name to list of names (Note* Order of this determines sampling order)
        self.sensor_names.append((name, num))

    def to_robot(self, key, reading):
        '''
            Transform a sensor reading to robot frame
        '''

        # Get proper transform by using key (name, num) to get right sensor
        T = self.s[key][2] # Transform is 3rd element in dictionary entry

        # Multiply reading by transform
        new_read = np.dot(T, np.array([reading, 0, 0, 1]).reshape((4, 1)))

        # # Print debug info to logger
        # logger.debug('Inside to_robot(): T: ', new_read)
        # logger.debug('Inside to_robot(): Sensor reading: ', np.array([reading, 0, 0, 1]).reshape((4, 1)))
        # logger.debug('Inside to_robot(): new_read: ', new_read)

        # Remove extra digit from end
        new_read = new_read.tolist()[:-1]

        # Return new reading (as a list)
        return new_read

    def numSensor(self, names):
        '''
            Returns the number of a type of sensor
        '''

        # Determine number of sensors with given names
        return len([x[0] for x in self.s.keys() if x[0] in names])

    def get_weights(self):
        '''
            Returns a list of sensor weights
        '''

        (_, weights, _) = (item for item in self.s)
        return weights

    def __str__(self):
        '''
            Returns instance arguments
        '''

        print "---- Sensor object .__str__ ----"

        print "self.sensor_names: ", self.sensor_names

        for k, v in self.s.iteritems():
            print k, " : ", v

        print "--------------------------------"
