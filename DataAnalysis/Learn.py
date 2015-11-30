# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program reads in Room object and clusters/connects areas in the room

from Room import Room
from Move import Move
from Area import Area

# Initialize room object
room = Room()

# Read in room object from text file
room.read_from_text('room2015-11-30.txt')

# Perform knn clustering on areas
room.cluster()

# Connect remaining areas with moves
room.connect_areas()
