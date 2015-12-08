import numpy as np
import cv2

class RGBHistogram:

    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        '''
            Function will return a feature vector representing histogram of an RGB image
        '''
        # Make a histogram using built in cv2 func
        hist = cv2.calcHist(
            [image], [0, 1, 2], None, self.bins, [0, 256, 0, 256, 0, 256])

        # Normalize the histogram
        hist = cv2.normalize(hist)

        # flatten the histogram and return ( make array with 3 columns of size
        # N be an array with one column of size 3N)
        return hist.flatten()

    def distance(hist_1, hist_2):
        '''
            Returns the distance between two given histogram feature vectors
        '''
