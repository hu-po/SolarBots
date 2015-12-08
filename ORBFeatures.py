import numpy as np
import cv2

class ORBFeatures:

    def describe(self, image):
        '''
            Function will return a feature vector representing ORB features of an RGB image
        '''

        # Initiate STAR detector
        orb = cv2.ORB()

        # find the keypoints with ORB
        kp = orb.detect(image, None)

        # compute the descriptors with ORB
        kp, des = orb.compute(image, kp)

        # Return descriptor vector
        return des

    def distance(des_1, des_2):
    '''
        Returns the distance between two given ORB feature vectors
    '''