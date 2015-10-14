# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Determines location of robot using pointcloud matching (from sonar sensors)

import numpy as np
import maptool
from python_mysql_connect import connect, insert_current_pos, query_current_pos
from brain import RAND_DIST_MU, RAND_DIST_SIGMA, RAND_ANG_MU, RAND_ANG_SIGMA, RAND_NUM
import pcl
from pcl.registration import icp, gicp, icp_nl


# Create map
# TODO: python pcl

def slamfunc(scan, curr_pos):

    # Convert scan to points
    scanpc = scan_to_points(scan)

    # Get map
    mapa = maptool.get_map()

    # Define best-guess transform using curr_pos

    # Use ICP to get true transform

    # Convert true transform into curr_pos format
    # pos_to_transform()

    # Generate perturbations from normal distribution
    pos_perturb = np.random.normal(RAND_DIST_MU, RAND_DIST_SIGMA, 2 * RAND_NUM).reshape(2, RAND_NUM)
    angle_perturb = np.random.normal(RAND_ANG_MU, RAND_ANG_SIGMA, RAND_NUM)

    print pos_perturb
    print angle_perturb

    # Perturb scans
    # TODO: This can probably be done with one tricky matrix multiplication

    # Iterate through perturbation scans
    for i in range(0, len(scan_perturb)):

        # Iterate through local map
        for j in range(0, len(mapa)):

            # Iterate through scan points
            for k in range(0, len(scan_perturb[i])):

                # compare scan point with local map points
                scan_perturb[i, k]

                # TODO: This might be faster with clever matrix functions

                # Get score, add it to aggregate score

        # compare aggregate score to other aggregate scores
                    # set lowest score to perturbation

    # correct current position using lowest score perturbation
    curr_pos = scan_perturb[score.index(min(score))]

    # Push new map data to database
    maptool.add_to_map(scan)

    return curr_pos


def main():
    return


if __name__ == '__main__':
    main()
