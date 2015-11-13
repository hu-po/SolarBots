# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Map (Mapa) class that contains map object, has update functions for storing in database

import pcl

# Map class
class Mapa:

    def __init__(self):
        
        # Pull map from database or create one
        self.pull_map()

    def pull_map():  # Downloads map from database and writes it to local file

        # Get map from database
        # TODO: Get map from database computer

        # Try to load map
        try:
            self.mapa = pcl.load("map.pcd")

        except IOError:

            # "empty" point cloud
            self.mapa = pcl.PointCloud() 

            # Save to local file
            pcl.save(self.mapa, "map.pcd")

    def push_map(self):  # Pushes map pointcloud to database and writes to local file

        # Push map to server
        # TODO: Push map to database computer

        # Store map as local .pcd file
        pcl.save(self.mapa, "map.pcd")    

    def add_to_map(self, points):  # Add a set of points to the map

        # Put new points into pointcloud and add to map
        self.mapa += pcl.PointCloud(points)

        # Filter the map
        self.filter_map()

        # Push map to database TODO: This might be slowing the system down
        self.push_map()

    def filter_map(self, mean=50, std_dev=1.0): # Apply a statistical filter to the map

        # Define filter
        fil = self.mapa.make_statistical_outlier_filter()
        fil.set_mean_k(mean)
        fil.set_std_dev_mul_thresh(std_dev)

        # Filter map
        self.mapa = fil.filter()

# -------- TEST CODE

mapa = Mapa()

# print out Map Cloud
print mapa.get_map()
