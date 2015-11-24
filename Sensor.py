# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Sensor class defines sensor objects, with location, type, etc

import numpy as np
from numpy import cos, sin

# TODO: Make an inherited class from Sensor called Reading, which stores
# information for a sensor reading

# Calculate the transformation to a frame


def calculateTransform(loc):

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


class Sensor:

    def __init__(self):

        # Initialize sensor dictionary
        self.s = {}

    def addSensor(self, name, num, weight, location):

        # Name, number, location (in robot frame), and transformation (to robot
        # frame) of sensor
        self.s[(name, num)] = (location, weight, calculateTransform(location))

    # Transform sonar sensor reading to robot frame
    def to_robot(self, key, reading):

        # Get proper transform by using key (name, num) to get right sensor
        (_, _, T) = self.s[key]

        # Multiply reading by transform
        new_read = np.dot(T, np.array([reading, 0, 0]).reshape((3, 1)))

        # Return new reading
        return new_read

    # Transform sonar sensor reading to global frame
    def to_global(key, reading):

        # TODO: Transform sensor reading to global frame

        new_read = np.dot(T, np.array([reading, 0, 0]).reshape((3, 1)))

        # Return new reading
        return new_read

    def numSensor(self, name):  # Returns the number of a type of sensor

        # Determine number of sensors with given name
        num = [x[0] for x in self.s.keys() if x[0] == name]

        return len(num)

    def get_weights(self):  # Returns a list of sensor weights
        (_, weights, _) = [item for item in self.s]
        return weights
