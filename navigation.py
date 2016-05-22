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

from __future__ import print_function

def navigate():
	'''
		Function will call exploration() function to move robot, but will keep
		track of previous moves
	'''

	# Test output
	print("Navigating ...")

	# Create motor and buzzer objects
	motor = Motor()
	buzzer = Buzzer()

	# Beep to indicate begining of navigate step
	buzzer.play(4)

	try:
		# Enter the exploration loop
		for i in xrange(params.p['MAX_ITER']):

			# Execute explore function and save results
			explore(motor, buzzer)

			# Wait between moves
			time.sleep(params.p['WAIT_TIME'])
	except Exception:
		pass
	finally:
		motor.stop_bot()
	  


def explore(motor, buzzer):
	'''
		Function will initialize and execute a new "move"

		Args:
			motor(motor_obj): used to control robot movement
			buzzer(buzzer_obj): signals start of exploration
	'''

	# Test output
	print "Exploring (moving to a new location) ..."

	# Beep to indicate begining of explore step
	buzzer.play(5)

	# Initialize new move object
	move = Move()

	# Vector of movement used
	move.get_move_vector()

	# Break down movement vector into motion primitives that robot can execute
	move.get_motion_plan()

	# Debug print move fields
	print(str(move))

	# Execute motion from given move primitives
	for (direction, amount) in move.primitives:
		print "Moving " + str(direction) + " " + str(amount)
		motor.move_bot(direction, distance=amount)


# ----------------------------------------------------
#           MAIN ROBOT SENSE-PLAN-ACT LOOP
# ----------------------------------------------------
if __name__ == '__main__':

	# TODO: Put options in here

	print "Starting navigation phase ..."
	navigate()
	print "Exited navigation phase ..."