import numpy as np
import matplotlib.pyplot as plt

from python_mysql_connect_jefe import connect, insert_pos_data, query_sensor_data, query_pos_data


# Colors/Size of the datapoints in the plot
PLOT_COLOR_HCSR04 = 'r' # Red
PLOT_SIZE_HCSR04 = 60
PLOT_COLOR_TSL2561 = 'b' # Blue
PLOT_SIZE_TSL2561 = 60
PLOT_COLOR_ROBOT = 'g' # Green
PLOT_SIZE_ROBOT = 200

def main():
	# Querry mysql database for robot position

	query_pos_data()

	x_robot = 0
	y_robot = 0

	# Querry mysql database for sensor data

	query_sensor_data()

	N = 5
	x_sonar = np.random.rand(N)
	y_sonar = np.random.rand(N)

	x_light = np.random.rand(N)
	y_light = np.random.rand(N)

	plt.scatter(x_robot, y_robot, s=PLOT_SIZE_ROBOT, c=PLOT_COLOR_ROBOT, alpha=0.5)
	plt.scatter(x_sonar, y_sonar, s=PLOT_SIZE_HCSR04, c=PLOT_COLOR_HCSR04, alpha=0.5)
	plt.scatter(x_light, y_light, s=PLOT_SIZE_TSL2561, c=PLOT_COLOR_TSL2561, alpha=0.5)
	plt.show()
