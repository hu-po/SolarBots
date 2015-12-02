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

    # Take pictures
    pics = takePics()

    # Initialize features list
    features = []

    for image in pics:

        # Get histogram and corner features for each image
        features.append((hist(image), ORB(image)))
        

    # Combine features list to form some kind of feature vector
        # - Going to need some kind of weighting here

    return features

def hist(image): # Returns a feature vector representing the histogram in an image

    return hist

def ORB(image): # Returns a feature vector using the OpenCV ORB feature detector

    img = cv2.imread('simple.jpg',0)

    # Initiate STAR detector
    orb = cv2.ORB()

    # find the keypoints with ORB
    kp = orb.detect(img,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0)
    plt.imshow(img2),plt.show()

    return feat

