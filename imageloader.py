from pyimagesearch.rgbhistogram import RGBHistogram
import argparse
import cPickle
import numpy as np
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="Path to directory that contains images")
ap.add_argument("-i", "--index", required=True,
                help="Path to where the computed index will be stored")

args = vars(ap.parse_args())

# load up the index and initialize search
index = cPickle.loads(open(args["index"]).read())
searcher = Searcher(index)

# loop through the images in the index
for (query, queryFeatures) in index.items():

    # perform search using current querry
    results = searcher.search(queryFeatures)

    # load the query image and display it
    path = args["dataset"] + "/%s" % (query)
    queryImage = cv2.imread(path)
    cv2.imshow("Query", queryImage)
    print "query: %s" % query

    # Initalize two montages (image "quilts")
    montageA = np.zeros((166 * 5, 400, 3), dtype="uint8")
    montageB = np.zeros((166 * 5, 400, 3), dtype="uint8")

    # loop over the top ten results
    for j in xrange(0, 10):
        (score, imageName) = results[j]
        path = args["dataset"] + "/%s" % imageName
        result = cv2.imread(path)
        print "\t%d. %s : %.3f" % (j + 1, imageName, score)

        # check to see if the first montage should be used
        if j < 5:
            montageA[j * 166:(j_ + 1) * 166, :] = result

        else:
            montageB[(j - 5) * 166:((j - 5) + 1) * 166, :] = result

    # Show the results
    cv2.imshow("Results 1-5", montageA)
    cv2.imshow("Results 6-10", montageB)
    cv2.waitKey(0)
