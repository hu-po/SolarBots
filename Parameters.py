# Project: https://github.com/HugoCMU/SolarTree
# Description: Parameters class defines parameter dictionary, which
# contains robot parameters


class Parameters:

    def __init__(self):

        # Initialize room dictionary
        self.p = {}  # Parameter
        self.d = {}  # Description

    def addParam(self, name, num, description):

        # Add room to room dictionary
        self.p[name] = num
        self.d[name] = description
