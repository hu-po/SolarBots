
import serial
import numpy as np
import datetime
from python_mysql_connect import connect, insert_data, query_commands
import motor

# Serial communication with Arduino
ser = serial.Serial('/dev/ttyACM0',  9600)

# Define constants
DATA_SAMPLE_SIZE = 3   # Sample size for data (increase to stabilize at cost of speed)
NUM_SONAR = 3  # Number of sonar sensors
NUM_LIGHT = 3   # Number of light sensors
MAX_ITER = 10   # Maximum number of Sense-Plan-Act Cycles

def sample():
    # print ser.readline()
    return ser.readline().split(',')


def readData():
    print "Reading data ..."

    # Create empty data array to store data
    data = np.empty([DATA_SAMPLE_SIZE, (NUM_SONAR + NUM_LIGHT)])

    # Populate empty data array
    for i in range(0, DATA_SAMPLE_SIZE):

        data[i, :] = sample()

    return data


def smoothData(data):

    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = np.empty([1, NUM_SONAR + NUM_LIGHT])

    # Simple median smoothing
    for i in range(0, NUM_SONAR + NUM_LIGHT):

        data_smooth[i] = np.median(data[:,i])

    # TODO: More ridiculous smoothing

    return data_smooth

def execute(commands):
    print "Executing commands from database ... "

    return


def main():

    print "Connecting to database ..."

    # Connect to MySQL database
    connect()

    print "Starting main loop ..."

    for i in range(0, MAX_ITER):

        # Read in raw data from sensors
        raw_data = readData()

        # Smooth raw data from sensors
        smooth_data = smoothData(raw_data)

        # Write data to MySQL
        for j in range(0, NUM_SONAR)
            insert_data( ('HC-SR04', j, smooth_data(j) , datetime.datetime.now()) ) # HC-SR04 Sensor

        for j in range(0, NUM_LIGHT)
            insert_data( ('TSL2561', j, smooth_data(NUM_SONAR + j) , datetime.datetime.now()) ) # TSL2561 Sensor

        # Get commands from MySQL and execute
        execute(query_commands())

        moveBot('forward', 1)  # Move forward 1 unit (10 cm)
        moveBot('turnleft', 1)  # Make one complete turn

    print "Exited main loop ..."
