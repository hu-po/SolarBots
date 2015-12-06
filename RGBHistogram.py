import numpy as np
import cv2


class RGBHistogram:

    # Constructor sets number of bins

    def __init__(self, bins):
        self.bins = bins

    def describe(self, image):
        # Make a histogram
        hist = cv2.calcHist(
            [image], [0, 1, 2], None, self.bins, [0, 256, 0, 256, 0, 256])

        # Normalize the histogram
        hist = cv2.normalize(hist)

        # flatten the histogram and return ( make array with 3 columns of size
        # N be an array with one column of size 3N)
        return hist.flatten()
