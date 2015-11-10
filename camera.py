# Author: Hugo P.
# Project: https://github.com/HugoCMU/SolarTree
# Description: Controls use of RPi Camera

from time import sleep
import numpy as np
import picamera
import cv2

# Initialize camera
camera = picamera.PiCamera() # TODO determine if this is the same datatype as an .imread('bleh.jpg')

# Take a test picture and show it
camera.capture('testimage.jpg')
camera.start_preview()
sleep(10)
camera.stop_preview()

# TODO: take picture and find features with OpenCV
	# Possibly use ORB feature detection for speed? Maybe FAST?

# --------- Code for FAST from online:

# Initiate FAST object with default values
fast = cv2.FastFeatureDetector()

# find and draw the keypoints
kp = fast.detect(img,None)
img2 = cv2.drawKeypoints(img, kp, color=(255,0,0))

# Print all default params
print "Threshold: ", fast.getInt('threshold')
print "nonmaxSuppression: ", fast.getBool('nonmaxSuppression')
print "neighborhood: ", fast.getInt('type')
print "Total Keypoints with nonmaxSuppression: ", len(kp)

cv2.imwrite('fast_true.png',img2)

# Disable nonmaxSuppression
fast.setBool('nonmaxSuppression',0)
kp = fast.detect(img,None)

print "Total Keypoints without nonmaxSuppression: ", len(kp)

img3 = cv2.drawKeypoints(img, kp, color=(255,0,0))

cv2.imwrite('fast_false.png',img3)


# --------- Code for ORB from online:

# Initiate STAR detector
orb = cv2.ORB()

# find the keypoints with ORB
kp = orb.detect(img,None)

# compute the descriptors with ORB
kp, des = orb.compute(img, kp)

# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0)
plt.imshow(img2),plt.show()