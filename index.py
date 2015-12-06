# import the necessary packages
from pyimagesearch.rgbhistogram import RGBHistogram
import argparse
import cPickle
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="Path to directory that contains images")
ap.add_argument("-i", "--index", required=True,
                help="Path to where the computed index will be stored")

args = vars(ap.parse_args())

# initialize the index dictionary to store our our quantifed
# images, with the 'key' of the dictionary being the image
# filename and the 'value' our computed features
index = {}

# Initiale an image descriptor
desc = RGBHistogram([8, 8, 8])

# Grab image path and loop through all images
for imagePath in glob.glob(args["dataset"] + "/*.png"):

    # Extract the unique "key" or image filename which we will use to store
    # the image histogram in the dictionary
    k = imagePath[imagePath.rfind("/") + 1:]

    # load image and get the feature vector
    image = cv2.imread(imagePath)
    features = desc.descriptor(image)
    index[k] = features

# Open up the file specified earlier in the args, and write the dictionary
# (converted to a string) into this file
f = open(args["index"], "w")
f.write(cPickle.dumps(index))
f.close()
