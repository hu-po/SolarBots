# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program reads in Room object and combines areas into more solid areas

# Initialize room object
room = Room()

# Read in room object from text file
room.read_from_text('Rooms/2015_11_22.txt')

# Loop through room object and gather areas

def cluster(areas, n): # Perform knn clustering on areas, returns clustered areas