import copy
import numpy as np
from storage import Constants as Constants
from helpers.FeatureCalculator import calculateFeatureForWindow


# Splits the emgData into augmented and not augmented data;
# Resulting data will look as followed:
#    [
#     [ [data_channel_1_aug_1][data_channel_2_aug_1] ... [data_channel_8_aug_1] ]
#        ...
#     [ [data_channel_1_last_aug][data_channel_2_last_aug] ... [data_channel_8_last_aug] ]
#    ]
# returns two of those fields: 1. augmented data, 2. not-augmented data
def splitRecordedSample(emgData, mods):
    splitAugData = []
    splitNoAugData = []

    for mod in mods:
        oneAugPart = []
        for channel in emgData:
            oneAugPart.append(np.array(channel[mod[0]: mod[1]]))
        if len(oneAugPart[0]) >= (Constants.samplesPerWindow + Constants.windowShift):
            splitAugData.append(oneAugPart)

    smallestNoAugIndex = 0
    emgData = np.asarray(emgData)
    for mod in mods:
        if (smallestNoAugIndex < len(emgData[0])) and \
                (len(emgData[0, smallestNoAugIndex:(mod[0] + 1)]) >=
                 (Constants.samplesPerWindow + Constants.windowShift)):
            dataSlice = emgData[:, smallestNoAugIndex:(mod[0] + 1)]
            splitNoAugData.append(dataSlice)
        smallestNoAugIndex = mod[1]
    # rest behind last mod part
    if (smallestNoAugIndex < len(emgData[0])) and \
            (len(emgData[0, smallestNoAugIndex:]) >=
             (Constants.samplesPerWindow + Constants.windowShift)):
        splitNoAugData.append(emgData[:, smallestNoAugIndex:])

    return splitAugData, splitNoAugData


# Creates the data for training the SVM
# param: augData    = storing the augmented data [[channels, data]]
#        noAugData  = storing the data representing no augmentation [channels, data]
# Splits the data into windows, calls the feature vector calculation for that window,
# adds the last two feature vectors to the current, to add some time aspect and
# labels everything with 'augmentation' or 'no augmentation'
# returns: X_train [[feature vector current window, last feature vector, feature vector before last]...]
#          y_train ['augmentation', ...]

def createMLData(augmentedData, noAugmentedData):
    X_train = []  # (n_samples, n_features)
    y_train = []  # (n_samples)->holding the labels/targets/classes

    # create feature vectors for augmented data
    index = 2
    for singleAugData in augmentedData:
        singleAugData = np.asarray(singleAugData)
        featureBeforeLast = calculateFeatureForWindow(singleAugData[:, 0:Constants.samplesPerWindow])
        lastFeature = calculateFeatureForWindow(
            singleAugData[:, Constants.windowShift:Constants.windowShift + Constants.samplesPerWindow])

        j = Constants.windowShift * 2

        while (j + Constants.samplesPerWindow <= len(singleAugData[0]) &
               len(singleAugData[0]) >= Constants.samplesPerWindow):
            currentFeature = calculateFeatureForWindow(singleAugData[:, j:j + Constants.samplesPerWindow])
            featureVector = currentFeature.tolist()
            featureVector.extend(copy.deepcopy(lastFeature))
            featureVector.extend(copy.deepcopy(featureBeforeLast))

            featureBeforeLast = copy.deepcopy(lastFeature)
            lastFeature = copy.deepcopy(currentFeature)

            X_train.append(np.asarray(featureVector))
            y_train.append("augmentation")

            j += Constants.windowShift

        index += 2

    # create feature vectors for no augmentation data
    index = 1
    for singleNoAugData in noAugmentedData:
        noAugFeatureBeforeLast = calculateFeatureForWindow(singleNoAugData[:, 0:Constants.samplesPerWindow])
        lastNoAugFeature = calculateFeatureForWindow(
            singleNoAugData[:, Constants.windowShift:Constants.windowShift + Constants.samplesPerWindow])
        currentIndex = Constants.windowShift * 2

        while (currentIndex + Constants.samplesPerWindow <= len(singleNoAugData[0])
               & len(singleNoAugData[0]) >= Constants.samplesPerWindow):
            currentNoAugFeature = calculateFeatureForWindow(
                singleNoAugData[:, currentIndex:currentIndex + Constants.samplesPerWindow])
            featureNoAugVector = currentNoAugFeature.tolist()
            featureNoAugVector.extend(copy.deepcopy(noAugFeatureBeforeLast))
            featureNoAugVector.extend(copy.deepcopy(lastNoAugFeature))

            noAugFeatureBeforeLast = copy.deepcopy(lastNoAugFeature)
            lastNoAugFeature = copy.deepcopy(currentNoAugFeature)
            X_train.append(np.asarray(featureNoAugVector))
            y_train.append("no augmentation")
            currentIndex += Constants.windowShift

        index += 2

    return X_train, y_train
