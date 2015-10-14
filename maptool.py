# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains functions to get and update the map

import numpy as np
import datetime
from python_mysql_connect import connect, query_map
from brain import FOG_RADIUS


def update_map():  # Downloads map from database and writes it to local file
    # Connect to database
    connect()

    # Get map from database
    mapa = query_map()

    # Store map as local xml file
    np.savetxt('map.txt', mapa)
    # http://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file


def get_map(pos):

    # Read local xml file containing map
    mapa = np.loadtxt('map.txt')

    # TODO: return only points within radius of current location.
    # for i in range(0, ln(mapa))

    # numpy.delete(mapa, (0), axis=0) # Delete 0th element along the 0th axis (rows)

    return mapa


def add_to_map():  # Add a set of points to the map
    return


def main():
    update_map()
    print get_map()

if __name__ == '__main__':
    main()
