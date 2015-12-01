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

    def lookup_area(self, area_name): # Find an area with an area name

        return area for area in self.areas if area.name = area_name else None

    def lookup_group(self, group_name): # Returns areas associated with a certain group

        # Get areas with 
        group = [area for area in self.areas if group_name in area.groups]

        return group

    # Finds the areas within defined fog radius of the given area
    def closest_areas(self, area):

        # Initialize closest areas, and smallest distance so far
        closest = []

        # Loop through all the areas in the room
        for area_iterator in self.areas:

            # Find distance between areas
            new_dist = area.distance_to_area(area_iterator)

            # If area is closer than current closest, re-assing
            if new_dist < params.p['FOG_RADIUS']:
                closest.append((area, new_dist))

        # Return the closest to position
        return closest

    def connect_areas(self): # Connect areas with moves according to fog radius

        # Loop through all the areas in the room    
        for area in self.areas:

            # Get closest areas to each area
            closest = self.closest_areas(area)

            # Loop through all the areas in list of closest
            for (close_area, distance) in closest:

                # Create virutal move between areas
                area.virtualmove(close_area)

    def cluster(self, n): # Perform knn clustering on areas, returns clustered areas

        # TODO: Cluster using:
        #   - Image feature vectors (Histogram, SIFT?)
        #   - Location

        # Each cluster will get a area group name
        clusters = []

        # Loop through all the clusters
        for i in range(len(clusters)):

            # Get group of areas
            group = clusters[i]

            # Initialize group name 
            group_name = ''.join(["GROUP_", random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3)])

            for area in group

                # Add group tag to member area
                area.groups.append[group_name]

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
