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

def takePics(): # TODO: take an array of pictures from camera

    # Create servo objects
    servo1 = Servo(1)
    servo2 = Servo(2)

    # Take 5 pictures, moving camera between
    servo1.setServo(0)
    servo2.setServo(0)

    camera.capture(rawCapture, format="rgb")

    servo1.setServo(0)
    camera.capture(rawCapture, format="rgb")

    servo1.setServo(0)
    camera.capture(rawCapture, format="rgb")

    servo1.setServo(0)
    camera.capture(rawCapture, format="rgb")

    servo1.setServo(0)
    camera.capture(rawCapture, format="rgb")

    # Return array of images
    return pics

















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