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

        # Initialize list of sensor names
        self.sensor_names = []

    def addSensor(self, name, num, weight, location):

        # Name, number, location (in robot frame), and transformation (to robot
        # frame) of sensor
        self.s[(name, num)] = (location, weight, calculateTransform(location))

        # Add sensor name to list of names (Note* Order of this determines sampling order)
        self.sensor_names.append((name, num))

    # Transform sensor reading to robot frame
    def to_robot(self, key, reading):

        # Get proper transform by using key (name, num) to get right sensor
        T = self.s[key][2] # Transform is 3rd element in dictionary entry

        # print T
        # print np.array([reading, 0, 0, 1]).reshape((4, 1))

        # Multiply reading by transform
        new_read = np.dot(T, np.array([reading, 0, 0, 1]).reshape((4, 1)))

        # print new_read

        # Remove extra digit from end
        new_read = new_read.tolist()[:-1]

        # Return new reading (as a list)
        return new_read

    # Transform sensor reading to global frame, requires position of robot in global frame
    def to_global(self, key, reading, pos):

        # Get global transformation matrix
        T_global = calculateTransform(pos)

        # Get robot frame transformation matrix using key (name, num) to get right sensor
        T_robot = self.s[key][2] # Transform is 3rd element in dictionary entry

        # Transform sensor reading to global frame
        new_read = np.dot(T_global, np.dot(T_robot, np.array([reading, 0, 0, 1]).reshape((4, 1))))

        # Remove extra digit from end
        new_read = new_read[:-1]

        # Return new reading (as a list)
        return new_read

    def numSensor(self, names):  # Returns the number of a type of sensor

        # Determine number of sensors with given names
        num = [x[0] for x in self.s.keys() if x[0] in names]

        return len(num)

    def get_weights(self):  # Returns a list of sensor weights
        (_, weights, _) = [item for item in self.s]
        return weights
