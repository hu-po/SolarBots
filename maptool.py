# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Contains functions to get and update the map

import numpy as np
from numpy import cos, sin
import math
import pcl
import datetime
from python_mysql_connect import connect, query_map
from brain import FOG_RADIUS, SENSOR_POS

def scan_to_points(scan, curr_pos): # Converts an explore scan into pointcloud object

    # Get xyz data from SENSOR_POS
    sensor_pos = np.array(SENSOR_POS)[:, 2:4]

    # Get sensor mask from SENSOR_POS
    sensor_mask = np.array(SENSOR_POS)[:, 5:]

    # Get scan as points in robot frame
    # TODO: scan_robot[i,:] = [sensor_pos[i, :] + sensor_mask[i, :] * scan[i], 1]

    # Convert scan points to global frame
    scan_global = scan_robot.dot(pos_to_transform(curr_pos).T)[:,:3]

    scanpc = pcl.PointCloud(scan_global)

    return scanpc

def pos_to_transform(pos): # Converts a robot state vector into a 3D transform

    # State vector is of form [X, Y, Theta]

    # Transformation for 3D Rotation along Z-Axis by Theta
    rotation = [[cos(pos[2]), -sin(pos[2]),  0,  0],
                [sin(pos[2]),  cos(pos[2]),  0,  0],
                [          0,            0,  1,  0],
                [          0,            0,  0,  1]]

    # Transformation for 3D Translation along X and Y Axis
    translation = [[1, 0, 0,  pos[0]],
                   [0, 1, 0,  pos[1]],
                   [0, 0, 1,       0],
                   [0, 0, 0,       1]]

    T = np.dot(translation, rotation)

    return T

def main():
    update_map()
    print get_map()

if __name__ == '__main__':
    main()
