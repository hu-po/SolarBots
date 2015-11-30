# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Area class defines area objects, which contain dictonaries
# of moves performed to reach and other information for that area

from brain import params
import numpy as np


class Area:

    def __init__(self):

        # Initialize dictionary of pictures
        self.pics = {}

        # Initialize position of area (X, Y, Z, and Theta)
        self.pos = [0, 0, 0, 0]

        # Previous areas (creating a graph)
        self.previous = []

        # Dictionary of moves to get from previous areas (measure of strength
        # of tie to previous area)
        self.moves_performed = []

    # Finds the distance from a position to a given area
    def distance_to_pos(self, given_pos):

        # Exact Distance from given_pos to this pos
        diff = np.subtract(np.array(self.pos), np.array(given_pos))

        # Distance number is a weighted average
        distance = np.sum(
            np.multiply(params.p('DISTANCE_WEIGHT'), np.absolute(diff)))

        # returns tuple containing exact value, and just the distance number
        return (distance, diff)

    # Finds the distance from an area to another area
    def distance_to_area(self, given_area):

        # Exact Distance from given_pos to this pos
        diff = np.subtract(np.array(self.pos), np.array(given_area.pos))

        # Distance number is a weighted average
        distance = np.sum(
            np.multiply(params.p('DISTANCE_WEIGHT'), np.absolute(diff)))

        # returns tuple containing exact value, and just the distance number
        return (distance, diff)
