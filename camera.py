# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Controls use of RPi Camera

from time import sleep
import numpy as np
import picamera
import cv2
import Servo
from brain import params

# Initialize camera
camera = picamera.PiCamera()
rawCapture = PiRGBArray(camera)

def takePics(): # Take an array of pictures using the camera

    # Create servo objects
    servo1 = Servo(1)
    servo2 = Servo(2)

    # Initialize picture list
    pics = []

    # Take 5 pictures, moving camera between
    for i in range(ser):
        servo1.setServo(params.p['CAMERA_SERVOS'][0][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][0][1])
        pics.append(camera.capture(rawCapture, format="rgb"))

        servo1.setServo(params.p['CAMERA_SERVOS'][0][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][0][1])
        camera.capture(rawCapture, format="rgb")

        servo1.setServo(params.p['CAMERA_SERVOS'][0][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][0][1])
        camera.capture(rawCapture, format="rgb")

        servo1.setServo(params.p['CAMERA_SERVOS'][0][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][0][1])
        camera.capture(rawCapture, format="rgb")

        servo1.setServo(params.p['CAMERA_SERVOS'][0][0])
        servo2.setServo(params.p['CAMERA_SERVOS'][0][0])
        camera.capture(rawCapture, format="rgb")

    # Return array of images
    return pics

def extractFeatures(): # Extract a feature vector from a series of images

    # TODO: SIFT features? (Histograms seems a bit savage)

    return features















# --------- Code for FAST from online:

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector()

# find and draw the keypoints
kp = fast.detect(img, None)
img2 = cv2.drawKeypoints(img, kp, color=(255, 0, 0))

# Print all default params
print "Threshold: ", fast.getInt('threshold')
print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
print "neighborhood: ", fast.getInt('type')
print "Total Keypoints with nonmaxSuppression: ", len(kp)

cv2.imwrite('fast_true.png', img2)

# Disable nonmaxSuppression
fast.setBool('nonmaxSuppression', 0)
kp = fast.detect(img, None)

print "Total Keypoints without nonmaxSuppression: ", len(kp)

img3 = cv2.drawKeypoints(img, kp, color=(255, 0, 0))

cv2.imwrite('fast_false.png', img3)

# --------- Code for ORB from online:

# Initiate STAR detector
orb = cv2.ORB()

# find the keypoints with ORB
kp = orb.detect(img, None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img, kp, color=(0, 255, 0), flags=0)
plt.imshow(img2), plt.show()
