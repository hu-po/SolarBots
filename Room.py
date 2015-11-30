# Project: https://github.com/HugoCMU/SolarTree
# Description: Room class defines room objects, which contain dictonaries
# of pictures and lists of areas for that room

import pickle
import datetime
from brain import params


class Room:

    def __init__(self):

        # Initialize dictionary of pictures
        self.room_pics = {}

        # List of areas in room
        self.areas = []

    # Finds the closest area associated with a position
    def closest_pos(self, area):

        # Initialize closest area, and smallest distance so far
        closest = None
        smallest_dist = params.p['FOG_RADIUS']

        # Loop through all the areas in the room
        for area_iterator in self.areas:

            # Find distance between areas
            new_dist = area.distance_to_area(area_iterator)

            # If area is closer than current closest, re-assing
            if new_dist < smallest_dist:
                closest = area
                smallest_dist = new_dist

        # Return the closest to position
        return closest

    # Loads a room from text file #TODO: eventually this has to be put in a database
    def load_room(filename):

        # Load room object from file using pickle
        f = open(filename)
        room = pickle.load(''.join([params.p['ROOM_PATH'], filename]))
        f.close()

        # Return room object
        return room

    # Stores a room_picsm to a text file #TODO: eventually put in database
    def store_room(self):

        # Get date
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Store room object in file using pickle
        f = open(''.join([params.p['ROOM_PATH'], 'room', date, '.pckl']), 'w')
        pickle.dump(self, f)
        f.close()
