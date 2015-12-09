# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Controls use of RPi Camera

from time import sleep
import numpy as np
import picamera
import cv2
import Servo
from brain import params
import RGBHistogram
import ORBFeatures

# Initialize camera
camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)

def takePics():
    '''
        Returns a list of pictures taken at positions specified in teh global parameter CAMERA_SERVOS
    '''

    # Create servo objects
    servo1 = Servo(1)
    servo2 = Servo(2)

    # Initialize picture list
    pics = []

    # Take 5 pictures, moving camera between
    for i in range(params.p['CAMERA_SERVOS']):
        servo1.setServo(params.p['CAMERA_SERVOS'][i][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][i][1])
        pics.append(camera.capture(rawCapture, format="rgb"))

    # Return array of images
    return pics

def extractFeatures():
    '''
        Extracts a list of feature vectors from a list of images
    '''

    # Take pictures
    pics = takePics()

    # Initialize features list
    features = []

    for image in pics:

        # Initialize image histogram object and get feature vector
        hist = RGBHistogram([8, 8, 8])
        hist_features = hist.descriptor(image)

        # Initialize ORB features object and get feature vector
        orb = ORBFeatures()
        orb_features = orb.descriptor(image)

        # Get histogram and corner features for each image
        features.append((hist_features, orb_features))

    # Combine features list to form some kind of feature vector
        # - Going to need some kind of weighting here

    return features

# def ORB(image): # Returns a feature vector using the OpenCV ORB feature detector

#     img = cv2.imread('simple.jpg',0)

#     # Initiate STAR detector
#     orb = cv2.ORB()

#     # find the keypoints with ORB
#     kp = orb.detect(img,None)

#     # compute the descriptors with ORB
#     kp, des = orb.compute(img, kp)

#     # draw only keypoints location,not size and orientation
#     img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0)
#     plt.imshow(img2),plt.show()

#     return feat

