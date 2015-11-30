# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room

# from python_mysql_connect import insert_sensor_data, insert_current_pos, query_current_pos

class Move:

    def __init__(self):

        # Initial position [X, Y, Z, Theta]
        self.initial_pos = [0, 0, 0, 0]

        # Calculated final position [X, Y, Z, Theta]
        self.final_pos = [0, 0, 0, 0]

        # Vector of movement used
        self.direction_vector = []

        # Rotation performed
        self.rot_angle = []

        # Distance traveled
        self.distance = []

        # Motion primitives to perform move
        self.primitives = []

        # Motion delta (delX, delY, delZ, delTheta)
        self.delta = [0, 0, 0, 0]

        # Sensor data for the move (populated in navigation.get_move_vector)
        self.raw_data = []
        self.smooth_data = []
        self.pos_vectors = []
        self.weighted_pos_vectors = []

    # Push information (along with reading) on the move to the database
    def push_to_database(self, smooth_data):

        # TODO: print this to mysql
        print "Push to database..."

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
