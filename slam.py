import numpy as np
import maptool
from python_mysql_connect import connect, insert_current_pos, query_current_pos

# Define parameters for distance/angle perturbations
RAND_DIST_MU = 0 # Center of distribution (cm)
RAND_DIST_SIGMA = 1 # Standard deviation (cm)
RAND_ANG_MU = 0 # Degrees
RAND_ANG_SIGMA = 10 # Degrees
RAND_NUM = 10 # Number of random samples

def slamfunc(scan, curr_pos, fog):

    # Get local map
    mapa = maptool.get_map(curr_pos, fog)

    # Generate perturbations from normal distribution
    pos_perturb = np.random.normal(RAND_DIST_MU, RAND_DIST_SIGMA, 2*RAND_NUM).reshape(2, RAND_NUM)
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


def navigate():
    # given a position? find somewhere to move which makes sense?
    # Somehow break these down into motion primitives?

    return


def main():
    return


if __name__ == '__main__':
    main()
