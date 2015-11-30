# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Visualizes areas and moves

import sys
sys.path.insert(0,'..')

import numpy as np
import matplotlib.pyplot as plt
from Room import Room
from Sensor import Sensor
from brain import params, sensors


# Colors/Size of the datapoints in the plot
PLOT_COLOR_HCSR04 = 'r'  # Red
PLOT_SIZE_HCSR04 = 60

PLOT_COLOR_TSL2561 = 'b'  # Blue
PLOT_SIZE_TSL2561 = 60

PLOT_COLOR_AREA = 'g'  # Green
PLOT_SIZE_AREA = 200

def plot_moves(move, axes): # Plots the moves to an area as vectors in 2D space

    # Initial position of move
    pos_i = move.initial_pos

    # Final position of move
    pos_f = move.final_pos

    # Plot arrow showing move
    axes.arrow(pos_i[0], pos_i[1], (pos_f[0] - pos_i[0]), (pos_f[1] - pos_i[1]), width=1.0)

    # Plot sensor scan data (loop through all the sensors)
    for i in range(len(sensors.sensor_names)):

        # Get sensor name using sensor name list
        sensor = sensors.sensor_names[i]

        # Get datapoint from move object
        data_point = move.global_pos_vectors[i]

        # Determine color based on sensor type
        if sensor == 'HCSR04':
            color = PLOT_COLOR_HCSR04
            size = PLOT_SIZE_HCSR04
        else:
            color = PLOT_COLOR_TSL2561
            size = PLOT_SIZE_TSL2561

        axes.scatter(data_point[0], data_point[1], s=size, c=color, alpha=0.7)


def plot_area(area, axes): # Plots an area as a red circle in space

    # Plot the area to axes handle
    axes.scatter(area.pos[0], area.pos[1], s=PLOT_SIZE_AREA, c=PLOT_COLOR_AREA, alpha=0.2)

    # Plot moves from previous area to this area
    for move in area.moves_performed:
        plot_moves(prev_move, axes)

    # Determine vectors for axes of area, transforming using theta (area.pos[3])
    x_axis = [cos(area.pos[3]), sin(area.pos[3])]
    y_axis = [-sin(area.pos[3]), cos(area.pos[3])]

    # Plot axes of robot on area so we can tell different orientations recorded
    axes.arrow(area.pos[0], area.pos[1], x_axis[0], x_axis[1], width=0.5)
    axes.arrow(area.pos[0], area.pos[1], y_axis[0], y_axis[1], width=0.5)

def main():

    # Initialize room object
    room = Room()

    # Read in room object from text file
    room.read_from_text('room2015-11-30.pckl')

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