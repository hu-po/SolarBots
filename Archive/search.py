import numpy as np


class Searcher:

    def __init__(self, index):
        self.index = index

    def search(self, queryFeatures):

        # initialize dictionary of results
        results = {}

        # loop over the index
        for (k, features) in self.index.items():

            # compute chi-squared distance
            d = self.chi2_distance(features, queryFeatures)

            # Update results dictionary with distance
            results[k] = d

        # Sort the results, with smallest distances in the front of the
        # dictionary
        results = sorted([(v, k) for (k, v) in results.items()])

        # return the results
        return results

    def chi2_distance(self, histA, histB, eps=1e-10):
        # compute the chi-quared distance
        d = np.sum([((a - b) ** 2) / (a + b + eps)
                    for (a, b) in zip(histA, histB)])

        # return distance
        return d
