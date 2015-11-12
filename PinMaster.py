# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: PinMaster class stores all of the pins in a PinMaster object

import numpy as np
from numpy import cos, sin

class PinMaster:

	def __init__(self):

		# Initialize sensor dictionary
		self.pins = {}

	def addPin(self, name, num):

		# Add pin number to pins dictionary using name as the key
		self.pins[name] = num
		