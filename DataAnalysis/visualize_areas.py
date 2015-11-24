# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Visualizes areas and moves

import numpy as np
import matplotlib.pyplot as plt
from Room import Room

# Colors/Size of the datapoints in the plot
PLOT_COLOR_HCSR04 = 'r'  # Red
PLOT_SIZE_HCSR04 = 60

PLOT_COLOR_TSL2561 = 'b'  # Blue
PLOT_SIZE_TSL2561 = 60

PLOT_COLOR_AREA = 'g'  # Green
PLOT_SIZE_AREA = 200

def plot_moves(move, ax): # Plots the moves to an area as vectors in 2D space

    # Initial position of move
    pos_i = move.initial_pos

    # Final position of move
    pos_f = move.final_pos

    # Plot arrow showing move
    ax.arrow(pos_i[0], pos_i[1], (pos_f[0] - pos_i[0]), (pos_f[1] - pos_i[1]), width=1.0)

    # Plot sensor scan data
    for sensorscan in move.sensordata:

        # Extract data from each element
        (sensor, x, y) = sensorscan

        # Determine color based on sensor type
        if sensor = 'HCSR04':
            color = PLOT_COLOR_HCSR04
            size = PLOT_SIZE_HCSR04
        else
            color = PLOT_COLOR_TSL2561
            size = PLOT_SIZE_TSL2561


        ax.scatter(x, y, s=size, c=color, alpha=0.7)


def plot_area(area, ax): # Plots an area as a red circle in space

    # Plot the area to axes handle
    ax.scatter(area.pos[0], area.pos[1], s=PLOT_SIZE_AREA, c=PLOT_COLOR_AREA, alpha=0.2)

    # Plot moves from previous area to this area
    for move in area.moves_performed:
        plot_moves(prev_move, ax)

    # TODO: Plot axes of robot on area so we can tell different orientations recorded


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

    # Initialize room object
    room = Room()

    # Read in room object from text file
    room.read_from_text('Rooms/2015_11_22.txt')

    # Initialize Figure
    fig, ax = plt.subplots()

    # Define plot parameters
    plt.xlim(-5, 5)
    plt.ylim(-5, 5)
    plt.xlabel('X')
    plt.xlabel('Y')

    # Plot the areas and moves within each room
    for area in room.areas:
        plot_area(area, ax)

    plt.show()

if __name__ == '__main__':
    main()