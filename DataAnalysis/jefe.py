import numpy as np
import matplotlib.pyplot as plt

from python_mysql_connect_jefe import connect, insert_pos_data, insert_sensor_data, query_raw_sensor_data, query_raw_pos_data
import visualize

# Connect to databse
connect()

# Querry raw sensor data 

query_raw_sensor_data()

# Querry raw robot position data

query_raw_pos_data() 

# Combine both 
# TODO: need to make a table with sensor data relative to robot, preferrably filtered

# Insert into database

# Visualize 