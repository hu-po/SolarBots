# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Program uses the sensors to determine best sequence of moves for robot to execute.

from brain import ser, params, sensors
from motor import Motor
from Buzzer import Buzzer
from Move import Move
import time

import numpy as np
import numpy.linalg as la

def navigate():
	'''
		Function will call exploration() function to move robot, but will keep
		track of previous moves
	'''

	# Test output
	print "Navigating ..."

	# Beep to indicate begining of navigate step
	buzzer = Buzzer()
	buzzer.play(4)

	# Create motor object
	motor = Motor()

	try:
		# Enter the exploration loop
		for i in xrange(params.p['MAX_ITER']):

			# Execute explore function and save results
			explore(motor)

			# Wait between moves
			time.sleep(params.p['WAIT_TIME'])
	except Exception:
		pass
	finally:
		motor.stop_bot()
	  


def explore(motor):
	'''
		Function will initialize and execute a new "move"
	'''

	# Test output
	print "Exploring (moving to a new location) ..."

	# Beep to indicate begining of explore step
	buzzer = Buzzer()
	buzzer.play(5)
	del buzzer

	# Initialize new move object
	move = Move()

	# Vector of movement used
	move = get_move_vector(move)

	# Break down movement vector into motion primitives that robot can execute
	move.getMotionPlan()

	# Debug print move fields
	str(move)

	# Execute motion from given move primitives
	for (direction, amount) in move.primitives:
		print "Moving " + str(direction) + " " + str(amount)
		motor.move_bot(direction, distance=amount, num=params.p['MOTOR_PWR'])


def sample():
	'''
		Sample Arduino sensors and return datapoints
	'''
	# Set timeout time (2 seconds)
	timeout = time.time() + params.p['TIMEOUT']

	# Initialize points list and begin loop
	points = []
	while len(points) != sensors.numSensor(['HC-SR04', 'TSL2561']):

		# Gather points from serial object
		points = ser.readline().strip().split(',')

		# If function times out, set points to empty array and break
		if time.time() > timeout:
			points = [0] * (sensors.numSensor(['HC-SR04', 'TSL2561']))
			break

	return points


def readData():
	print "Reading data ..."

	# Create empty data list to store data
	data = []

	# Populate empty data array
	for i in xrange(params.p['DATA_SAMPLE_SIZE']):
		data.append(sample())

	return data


def smoothData(data):
	print "Smoothing data ..."

	# Create empty data array to store smooth data
	data_smooth = []

	# # Test print
	# print "Data: ", data

	# Simple median smoothing
	for i in xrange(len(data[0])):

		# Make a list of all the different readings from one
		strip = [int(sample[i]) for sample in data]

		# Add them to data_smooth
		data_smooth.append(np.median(strip))

	return data_smooth


def get_move_vector(move):
	'''
		Performs movement based on gradient direction of sensor readings.
		Returns vector direction of movement
	'''

	# Read and Smooth raw data from sensors
	move.smooth_data = smoothData(readData())

	# Combine readings together using sensor weights
	for data, sensr in zip(move.smooth_data, sensors.s.iterkeys()):

		# Determine position vector for sensor data (with respect to robot frame)
		pos_vector = sensors.to_robot(sensr, data)

		# Second element in sensor dictionary entry is sensor weight
		sensor_weight = sensors.s[sensr][1]

		# Multiply pos readings by sensor weight
		weighted_vector = np.multiply(sensor_weight, pos_vector).tolist()

		move.weighted_pos_vectors.append(weighted_vector)

		# Debug print statements
		# print "sensr, ", sensr
		# print "data, ", data
		# print "pos_vector, ", pos_vector
		# print "sensor_weight, ", sensor_weight
		# print "weighted_vector, ", weighted_vector

	# Combine weighted position vectors to get ultimate direction vector
	move.direction_vector = np.mean(np.array(move.weighted_pos_vectors), axis=0)

	# Return move object
	return move

# ----------------------------------------------------
#           MAIN ROBOT SENSE-PLAN-ACT LOOP
# ----------------------------------------------------

print "Starting navigation phase ..."

navigate()

print "Exited navigation phase ..."