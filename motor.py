import RPi.GPIO as GPIO
import serial
import numpy as np
from python_mysql_connect import connect, insert_data, query_commands

from time import sleep

GPIO.setmode(GPIO.BOARD)
ser = serial.Serial('/dev/ttyACM0',  9600)

# Define constants
DATA_SAMPLE_SIZE = 3   # Sample size for data (increase to stabilize at cost of speed)
SEC_PER_TURN = 3   # Seconds required to complete one full turn
SEC_PER_MOVE = 4   # Seconds required to move 10cm
NUM_SONAR = 3  # Number of sonar sensors
NUM_LIGHT = 3   # Number of light sensors
MAX_ITER = 10   # Maximum number of Sense-Plan-Act Cycles

# Define motor pins
Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 23
Motor2B = 21
Motor2E = 19

# Setup motor pin output
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)


def sample():
    # print ser.readline()
    return ser.readline().split(',')


def readData():
    print "Reading data ..."

    # Create empty data array to store data
    data = np.empty((NUM_SONAR + NUM_LIGHT, DATA_SAMPLE_SIZE))

    # Populate empty data array
    for i in range(0, DATA_SAMPLE_SIZE):

        data[i, :] = sample()

    return data


def smoothData(data):

    print "Smoothing data ..."

    # Create empty data array to store smooth data
    data_smooth = np.empty((NUM_SONAR + NUM_LIGHT, 1))

    # Simple median smoothing
    for i in range(0, NUM_SONAR + NUM_LIGHT):

        data_smooth[i, :] = np.median(data[:, i])

    # TODO: More ridiculous smoothing

    return data_smooth


def moveBot(direction, distance):

    if direction == 'forward':
        print "Going forwards ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_MOVE)

    elif direction == 'backward':
        print "Going backwards ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_MOVE)

    elif direction == 'turnleft':
        print "Turning Left ..."

        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.LOW)
        GPIO.output(Motor2B, GPIO.HIGH)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_TURN)

    elif direction == 'turnright':
        print "Turning Right ..."

        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
        GPIO.output(Motor1E, GPIO.HIGH)

        GPIO.output(Motor2A, GPIO.HIGH)
        GPIO.output(Motor2B, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.HIGH)

        sleep(distance / SEC_PER_TURN)

    else:
        print "ERROR: Wrong direction input"

    print "Stopping ..."
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)

    GPIO.cleanup()
    return


def execute(commands):
    print "Executing commands from database ... "

    return


def main():

    # Connect to MySQL database
    connect()

    print "Starting main loop ..."

    for i in range(0, MAX_ITER):

        # Read and Smooth data from sensor
        data = smoothData(readData())

        # Write data to MySQL
        insert_data(data)

        # Get commands from MySQL and execute
        execute(query_commands())

        moveBot('forward', 1)  # Move forward 1 unit (10 cm)
        moveBot('turnleft', 1)  # Make one complete turn

    print "Exited main loop ..."
