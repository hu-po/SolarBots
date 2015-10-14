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


def pull_map():  # Downloads map from database and writes it to local file

    # Get map from database
    # TODO: Get map from database computer

    # Store map as local .pcd file
    # pcl.save(mapa, "map.pcd")

    # For now this function will just initialize a blank map
    initialize_map()

def push_map(mapa):  # Pushes map pointcloud to database and writes to local file

    # Get map from database
    # TODO: Get map from database computer

    # Store map as local .pcd file
    pcl.save(mapa, "map.pcd")
    

def get_map(): # Loads map from local file and returns pointcloud object

    # Load local .pcd file containing map
    mapa = pcl.load("map.pcd")

    # TODO: return only points within radius of current location.
    # for i in range(0, ln(mapa))

    # numpy.delete(mapa, (0), axis=0) # Delete 0th element along the 0th axis (rows)

    return mapa


def add_to_map(mapa, points):  # Add a set of points to the map

    # Add points to map

    # Filter the map
    filter_map()

    # Push map to database
    push_map()

    return mapa

def filter_map(mapa, mean=50, std_dev=1.0): # Apply a statistical filter to the map

    fil = mapa.make_statistical_outlier_filter()
    fil.set_mean_k(mean)
    fil.set_std_dev_mul_thresh(std_dev)
    
    return fil.filter()

def initialize_map(): # Initializes an empty map

    p = pcl.PointCloud()  # "empty" point cloud

    # Save to local file
    p.save("map.pcd")

    return

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
