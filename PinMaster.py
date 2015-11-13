# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: PinMaster class stores all of the pins in a PinMaster object

class PinMaster:

	def __init__(self):

		# Initialize sensor dictionary
		self.p = {}

	def addPin(self, name, num):

		# Add pin number to pins dictionary using name as the key
		self.p[name] = num
		