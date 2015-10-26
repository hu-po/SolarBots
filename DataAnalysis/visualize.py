import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import sys
# sys.path.append("..")
# from python_mysql_connect import query_sensor_data, query_current_pos

# Colors/Size of the datapoints in the plot
PLOT_COLOR_HCSR04 = 'r'  # Red
PLOT_SIZE_HCSR04 = 60
PLOT_COLOR_TSL2561 = 'b'  # Blue
PLOT_SIZE_TSL2561 = 60
PLOT_COLOR_ROBOT = 'g'  # Green
PLOT_SIZE_ROBOT = 200

# Initialize Figure
fig, ax = plt.subplots()

def update(data): # Update plot

    # Querry mysql database for robot position and sensor data
    # pos_data = query_current_pos() X_pos, Y_pos, Theta
    # sensor_data = query_sensor_data() SensorType, SensorNum, Reading, Date

    # Split into sonar and light data
    sonar = [x[2] for x in files if x[1] == 'HC-SR04']
    light = [x[2] for x in files if x[1] == 'TSL2561']


    # TODO: finish extracting positions from data
    
    # Extract robot position
    x_robot = 0
    y_robot = 0

    # Extract sensor data
    N = 5
    x_sonar = np.random.rand(N)
    y_sonar = np.random.rand(N)

    x_light = np.random.rand(N)
    y_light = np.random.rand(N)

    # Add new points to plot
    ax.scatter(x_robot, y_robot, s=PLOT_SIZE_ROBOT, c=PLOT_COLOR_ROBOT, alpha=0.5)
    ax.scatter(x_sonar, y_sonar, s=PLOT_SIZE_HCSR04, c=PLOT_COLOR_HCSR04, alpha=0.5)
    ax.scatter(x_light, y_light, s=PLOT_SIZE_TSL2561, c=PLOT_COLOR_TSL2561, alpha=0.5)

def main():

    # Define plot parameters
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel('X')
    plt.xlabel('Y')

    # Animate figure
    ani = animation.FuncAnimation(fig, update, interval=100)
    plt.show()

if __name__ == '__main__':
    main()


