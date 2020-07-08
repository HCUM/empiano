from math import sqrt
import numpy as np

def calculateRMS(data):
    return sqrt(sum(n*n for n in data) / len(data))


def pairwiseRatio(rmsDataOneWindow):
    ratios = []
    for i in range(len(rmsDataOneWindow)):
        for j in range(i, len(rmsDataOneWindow)):
            if i != j:
                ratios.append(rmsDataOneWindow[i] / rmsDataOneWindow[j])
    return ratios


#This method is called for calculating the feature vector for the given window data
#param: windowData = [channels, data_for_one_window]
def calculateFeatureForWindow(windowData, ratio=True):
    rmsData    = []
    for channel in windowData:
        rmsData.append(calculateRMS(channel))

    featureVec = rmsData
    if ratio: featureVec = np.concatenate([featureVec, pairwiseRatio(rmsData)], axis=None)
    return featureVec