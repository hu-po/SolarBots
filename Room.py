# Project: https://github.com/HugoCMU/SolarTree
# Description: Room class defines room objects, which contain dictonaries
# of pictures and lists of areas for that room

import cPickle
import datetime
from brain import params


class Room:

    def __init__(self):

        # Initialize dictionary of pictures
        self.room_pics = {}

        # List of areas in room
        self.areas = []

        # Current area (where robot is)
        self.current_area = []

    def lookup_area(self, area_name):
        '''
            Returns area within Room object with given area_name
        '''
        for area in self.areas:
            if area.name == area:
                return area

        # return None if area not found
        return None

    def lookup_group(self, group_name):
        '''
            Returns list of areas within Room object within a group
            of given group_name
        '''
        group = [area for area in self.areas if group_name in area.groups]

        return group

    def closest_areas(self, area):
        '''
            Returns lits of areas within Room object that lie within
            the fog radius (global parameter) of a given area
        '''

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

    def connect_areas(self):
        '''
            Connects (creates moves between) all areas within Room object
            that lie within the fog radius (global parameter) of a given area
        '''

        # Loop through all the areas in the room
        for area in self.areas:

            # Get closest areas to each area
            closest = self.closest_areas(area)

            # Loop through all the areas in list of closest
            for (close_area, distance) in closest:

                # Create virutal move between areas
                area.virtualmove(close_area)

    def localize(self):
        '''
            Function will return the "Best Matching Area" within the fog radius (global parameter)
            of the given area. Distance is calculated through 
        '''

        # Take pictures of the area
        new_area.pics = camera.takePics()

        # Extract feature vectors from the pictures
        new_area.feature_vec = camera.extractFeatures(new_area.pics)

        # Search other areas within the Fog Radius for matching features
        ORBFeatures.distance()
        RGBHistogram.distance()
        
        # Update family tag for the area based on other area's family tags

        # Determine best fit area

        # If best fit area passes certain threshold criteria
            # new_area is actually this already known "best fit" area


    def cluster(self, n):
        '''
            Performs knn clustering on areas, placing them in groups
        '''

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
            group_name = ''.join(["GROUP_", [random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(3)]])

            for area in group:

                # Add group tag to member area
                area.groups.append[group_name]


    def load_room(self, filename):
        '''
            Loads Room object of a given file name file path (global parameter) using pickle
        '''

        f = open(''.join([params.p['ROOM_PATH'], filename]), 'rb')
        self = cPickle.load(f)
        f.close()

    def store_room(self):
        '''
            Stores Room object to a file path (global parameter) using pickle
        '''

        print self.areas

        # Get date
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Store room object in file using pickle
        f = open(''.join([params.p['ROOM_PATH'], 'room', date, '.pckl']), 'w')
        f.write(cPickle.dumps(self))
        f.close()


    def describe(self):
        '''
            Prints out information about the room, such as list of areas, etc
        '''

        print "Room has " + str(len(self.areas)) + " areas: "
        print self.areas
