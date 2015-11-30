# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Area class defines area objects, which contain dictonaries
# of moves performed to reach and other information for that area

from brain import params
from Move import Move
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

    def virutal_move(self, origin_area): # Create a virutal move from an origin area
    
        # Create new move object
        move = Move()

        # Make sure move is set as a virtual move
        move.type = "Virtual"

        # Link areas together
        self.previous = area1

        # Set initial and final positions of move
        move.initial_pos = origin_area.pos
        move.final_pos = self.pos

        # Get the direction vector for the move between the two areas
        move.direction_vector = [final - initial for final, initial in zip(move.final_pos[:-1], move.initial_pos[:-1])]

        # Fill in other fields in the virutal area
        move.getMotionPlan()

        # Add move to area2's dictionary of moves
        self.moves_performed.append(move)
