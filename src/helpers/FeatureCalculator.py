import numpy as np
from math import sqrt


# Calculates the root-mean-square for the given data (data = 1-D array)
def calculateRMS(data):
    return sqrt(sum(n * n for n in data) / len(data))


# Calculates the pairwise ratios of the RMS values (one for each channel) for one window
# (every channel with all the others)
def pairwiseRatio(rmsDataOneWindow):
    ratios = []
    for i in range(len(rmsDataOneWindow)):
        for j in range(i, len(rmsDataOneWindow)):
            if i != j:
                ratios.append(rmsDataOneWindow[i] / rmsDataOneWindow[j])
    return ratios


# This method is called for calculating the feature vector for the given window data
# param: windowData = [[channel 1]...[channel n]] (data for one window)
# returns: featureVector = [rms_channel_1, ..., rms_channel_n, ratios]
def calculateFeatureForWindow(windowData, ratio=True):
    rmsData = []
    for channel in windowData:
        rmsData.append(calculateRMS(channel))

    featureVec = rmsData
    if ratio: featureVec = np.concatenate([featureVec, pairwiseRatio(rmsData)], axis=None)
    return featureVec
