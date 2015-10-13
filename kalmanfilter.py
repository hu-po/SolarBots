# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Applies a Kalman Filter to the robot state measurements

import numpy as np
from brain import OBSERVATION_NOISE

H = np.identity(3) # Observation model
P_0 = np.identity(3) # Initial estimate covariance
Q = np.zeros((3,3)) # Covariance of the process noise
R = OBSERVATION_NOISE * np.identity(3) # Covariance of the observation noise

F = np.identity(3) # State model
B = np.identity(3) # Control input model

# Definitions
# x_k_p = predicted state at k
# x_k_u = updated state at k
# x_km1_u = updated state at k - 1
# u_k = control input at k
# P_k_p = predicted estimate covariance at k
# P_km1_u = updated estimate covariance at k - 1
# z_k = measured state at k
# K_k = optimal kalman gain at k
# S_k = innovation covariance at k
# y_k = innovation at k

def kalman(curr_pos, curr_meas, curr_input, curr_cov=P_0):

	# Put arguments into matrix-named variables
	x_k_p = curr_pos
	P_k_p = curr_cov
	u_k = curr_input
	z_k = curr_meas

	# Predict Step
	x_k_p = F * x_km1_u + B * u_k
	P_k_p = F * P_km1_u * F.transpose() + Q

	# Update Step
	y_k = z_k - H * x_k_p
	S_k = H * P_k_p * H.tranpose() + R
	K_k = P_k_p * H * np.linalg.inv(S_k)
	x_k_u = x_k_p + K_k * y_k
	P_k_u = (np.identity(3) - K_k * H) * P_k_p

	# Update variables
	curr_pos_filtered = x_k_u
	curr_cov_filtered = P_k_u

	# Return appropriate variables
	return curr_pos_filtered, curr_cov_filtered

def main():

	curr_pos = np.array([0,0,0]).reshape(-1,1)
	curr_meas = np.array([12,0,0]).reshape(-1,1)
	curr_input = np.array([10,0,0]).reshape(-1,1)

    curr_pos_filtered, curr_cov_filtered = kalman(curr_pos, curr_meas, curr_input)

    print curr_pos
    print curr_meas
    print curr_input
    print curr_pos_filtered
    print curr_cov_filtered

if __name__ == '__main__':
    main()