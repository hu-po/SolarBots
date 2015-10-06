
import serial
import numpy as np
import datetime
from python_mysql_connect import connect, insert_sensor_data, insert_current_pos, query_current_pos
import motor
import maptool
import slam

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Define constants
DATA_SAMPLE_SIZE = 3   # Sample size for data (increase to stabilize at cost of speed)
NUM_SONAR = 3  # Number of sonar sensors
NUM_LIGHT = 3   # Number of light sensors
MAX_ITER = 10   # Maximum number of Sense-Plan-Act Cycles
MOTOR_PWR = 30  # 0 - 100 speed of motor
EXPLORE_ITER = 4 # Number of sensor readings in an explore scan
FOG_RADIUS = 100 # Radius of section of map to use (centered around current position) for SLAM

def sample():
    points = []
    while len(points) != 6:
        points = ser.readline().strip().split(',')
        #print points
        #print len(points)
        #print "garbage"
    return points


def readData():
    print "Reading data ..."

    # Create empty data array to store data
    data = np.empty([DATA_SAMPLE_SIZE, (NUM_SONAR + NUM_LIGHT)])

    # Populate empty data array
    for i in range(0, DATA_SAMPLE_SIZE):

        # print data(i,:)
        data[i, :] = sample()

    return data


def smoothData(data):

    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = np.empty([1, NUM_SONAR + NUM_LIGHT])

    # Simple median smoothing
    for i in range(0, NUM_SONAR + NUM_LIGHT):

        data_smooth[i] = np.median(data[:, i])

    # TODO: More ridiculous smoothing

    return data_smooth


def explore():
    print "Exploring current location ..."

    # Perform exploration movement
    motor.moveBot('forward', 1, MOTOR_PWR)  # Move forward 1 unit (10 cm)

    # Initialize exploration results matrix
    explore_results = []

    for i in range(0, EXPLORE_ITER)

        # Read in raw data from sensors
        raw_data = readData()

        # Smooth raw data from sensors
        smooth_data = smoothData(raw_data)

        print raw_data
        print smooth_data

        # Write data to MySQL
        # for j in range(0, NUM_SONAR):
        # HC-SR04 Sensor
        #     insert_sensor_data(('HC-SR04', j, smooth_data(j), datetime.datetime.now()))

        # for j in range(0, NUM_LIGHT):
        # TSL2561 Sensor
        #     insert_sensor_data(('TSL2561', j, smooth_data(NUM_SONAR + j), datetime.datetime.now()))

        # Store smooth data in exploration results matrix
        explore_results[i, :] = smooth_data

        # Rotate robot to get another set of data
        motor.moveBot('turnleft', 45, MOTOR_PWR)  # Make a 45 degree turn

    return explore_results


def main():

    print "Connecting to database ..."
    # connect()

    print "Starting motor GPIO connection ..."
    motor.start()

    print "Downloading latest map from database ..."
    # maptool.update_map()

    print "Starting main loop ..."

    for i in range(0, MAX_ITER):

        # Get current robot pose from database
        curr_pos = query_current_pos()

        # Explore (get dataset of points)
        scan = explore()

        # Use current position and explore dataset to determine new location
        # curr_pos = slamfunc(scan, curr_pos, FOG_RADIUS)

        # Push new robot pose to database
        insert_current_pos(curr_pos)

    print "Exited main loop ..."

    print "Clean up motor GPIO ..."
    motor.clean()

if __name__ == '__main__':
    main()
