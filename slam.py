import numpy as np
import maptool
from python_mysql_connect import connect, insert_current_pos, query_current_pos


def slamfunc(scan, curr_pos, fog):

	# Get local map
	mapa = maptool.get_map(curr_pos, fog)

	# Create perturbation scans

	# Iterate through perturbation scans

			# Iterate through local map

				# Iterate through scan points

					# compare scan point with local map points
					# Get score, add it to aggregate score

			# compare aggregate score to other aggregate scores
			# set lowest score to perturbation

	# correct current position using lowest score perturbation

	# update current position
	
	# Push new map data to database
	maptool.add_to_map(scan)

	return curr_pos

def navigate():
	# given a position? find somewhere to move which makes sense?
	# Somehow break these down into motion primitives?

def main():

if __name__ == '__main__':
    main()
