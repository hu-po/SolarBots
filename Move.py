# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room


class Move:

    def __init__(self):

        # Initial position
        self.initial_pos = []

        # Calculated final position
        self.final_pos = []

        # Vector of movement used
        self.move_vector = []

        # Rotation performed
        self.rot_angle = []

        # Distance traveled
        self.distance = []

    def push_to_database(self, smooth_data): # Push information (along with reading) on the move to the database

            # TODO: print this to mysql

            # Write data to MySQL
#         for j in range(0, sensors.numSensor('HC-SR04')):
# HC-SR04 Sensor
# print 'HC-SR04'
# print j
# print smooth_data[j]
# print datetime.datetime.now()
#             insert_sensor_data(('HC-SR04', j + 1, smooth_data[j][0], datetime.datetime.now()))

#         for j in range(0, sensors.numSensor('TSL2561')):
# TSL2561 Sensor
# print 'TSL2561'
# print NUM_SONAR + j
# print smooth_data[NUM_SONAR + j]
# print datetime.datetime.now()
#             insert_sensor_data(('TSL2561', j + 1, smooth_data[sensors.numSensor('HC-SR04') + j][0], datetime.datetime.now()))


'''
Create a linked list of waypoints. graph with nodes and connections.

Then you create a counter which counts how many times you have visited the node.

Nodes are called rooms. Rooms contain cdictionaries of pictures, which contain images and sonar readings

Use the sonar kind of like a sa vector field to slowly drive in the direction away from obstacles, pseudo randomly

Then take a bunch of pictures "Sampling" a location, and creating a new node within the graph.

These nodes will have to be stored with a database (or initially as a text file).

These nodes will then continue to be used, but we will look at all the nodes in teh graph and "Purge" the lowest 10 nodes with the lowest visit count.

We can then check similarity between all the nodes, and group then using knn groups and position, into supernodes.

We then consolidate our graph with that graph and slowly build a model of the room.

Store other variables in these nodes (combined with the array of connected nodes).



Then



Small robots, with two wheel motors and a motor allowing the top of it to move freely (basically a kiva bot). Actually this whole idea is just Kivabots
that are small and you can place under your furniture and the stuff in your house, then you can use a phone app to condense all your stuff to one side of the room

Okay sized robots that move pallets around in your warehouse.
'''