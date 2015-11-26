# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Each move object contains information on the move that
# brought robot from previous room to this next room

# from python_mysql_connect import insert_sensor_data, insert_current_pos, query_current_pos

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

        # Motion primitives to perform move
        move.primitives = []

        # Sensor sweep for the move (each element is a list (sensor,x,y) where x,y is in global frame)
        self.sensordata = []

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
