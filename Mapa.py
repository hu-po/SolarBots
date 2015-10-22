# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Map class that contains map object, has get and set functions

import numpy as np
import pcl

# Map class
class Mapa:

    description = "Map class handles map objects"

    def __init__(self):
        
        # Try to load map
        try:
            self.mapa = pcl.load("map.pcd")

        except IOError:

            # "empty" point cloud
            self.mapa = pcl.PointCloud()  

            # Save to local file
            pcl.save(mapa, "map.pcd")

    def pull_map():  # Downloads map from database and writes it to local file

        # Get map from database
        # TODO: Get map from database computer

        # Store map as local .pcd file
        # pcl.save(mapa, "map.pcd")

    def push_map(self):  # Pushes map pointcloud to database and writes to local file

        # Push map to server
        # TODO: Push map to database computer

        # Store map as local .pcd file
        pcl.save(mapa, "map.pcd")
        

    def get_map(): # Returns map object
        return self.mapa


    def add_to_map(self, points):  # Add a set of points to the map

        # Add points to map
        # TODO: add poitns to map

        # Filter the map
        filter_map()

        # Push map to database
        push_map()

        return mapa

    def filter_map(self, mean=50, std_dev=1.0): # Apply a statistical filter to the map

        # Define filter
        fil = self.mapa.make_statistical_outlier_filter()
        fil.set_mean_k(mean)
        fil.set_std_dev_mul_thresh(std_dev)
        
        # Update map
        # TODO: Update map

        return fil.filter()

    def describe(self,text):
        self.description = text

# -------- TEST CODE

mapa = Mapa()

# print out Map Cloud
print mapa.get_map()
