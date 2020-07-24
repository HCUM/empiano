import copy
import numpy as np
from storage import Constants as constants
from helpers.FeatureCalculator import calculateFeatureForWindow


'''
Splits the emgData into augmented and not augmented data;
resulting data will look as followed:
   [
    [ [data_channel_1_aug_1][data_channel_2_aug_1] ... [data_channel_8_aug_1] ]
       ...
    [[data_channel_1_last_aug][data_channel_2_last_aug] ... [data_channel_8_last_aug] ]
   ]
returns two of those fields: 1. augmented data, 2. non-augmented data
'''
def splitRecordedSample(emgData, mods):
    splittedAugData     = []
    splittedNonAugData  = []

    for mod in mods:
        oneAugPart  = []
        for channel in emgData:
            oneAugPart.append(np.array(channel[mod[0]: mod[1]]))
        splittedAugData.append(oneAugPart)

    smallestNonAugIndex = 0
    emgData = np.asarray(emgData)
    for mod in mods:
        slice = emgData[:, smallestNonAugIndex:mod[0]]
        splittedNonAugData.append(slice)
        smallestNonAugIndex = mod[1]

    if smallestNonAugIndex < len(emgData[0]):
        slice = emgData[:, smallestNonAugIndex:]
        splittedNonAugData.append(slice)

    return splittedAugData, splittedNonAugData


'''
Creates the data for training the SVM
param: augData    = storing the augmented data [[channels, data]]
       nonAugData = storing the data representing no augmentation [channels, data]
Splits the data into windows, calls the feature vector calculation for that window,
adds the last two feature vectors to the current, to add some time aspect and
labels everything with 'augmentation' or 'no augmentation'
returns: X_train [[feature vector current window, last feature vector, feature vector before last]...]
         y_train ['augmentation', ...]
'''
def createMLData(augmentedData, noAugmentedData):
    X_train = []  #(n_samples, n_features)
    y_train = []  #(n_samples)->holding the lables/targets/classes

    #create feature vectors for augmented data
    index = 2
    for singleAugData in augmentedData:
        singleAugData = np.asarray(singleAugData)
        featureBeforeLast = calculateFeatureForWindow(singleAugData[:, 0:constants.samplesPerWindow])
        lastFeature = calculateFeatureForWindow(
            singleAugData[:, constants.windowShift:constants.windowShift+constants.samplesPerWindow])

        j = constants.windowShift *2

        while (j + constants.samplesPerWindow <= len(singleAugData[0]) &
               len(singleAugData[0]) >= constants.samplesPerWindow):

            currentFeature = calculateFeatureForWindow(singleAugData[:, j:j + constants.samplesPerWindow])
            featureVector = currentFeature.tolist()
            featureVector.extend(copy.deepcopy(lastFeature))
            featureVector.extend(copy.deepcopy(featureBeforeLast))

            featureBeforeLast = copy.deepcopy(lastFeature)
            lastFeature = copy.deepcopy(currentFeature)

            X_train.append(np.asarray(featureVector))
            y_train.append("augmentation")

            j+= constants.windowShift

        index += 2

    #create feature vectors for not augmented data
    index = 1
    for singleNoAugData in noAugmentedData:
        nonAugFeatureBeforeLast = calculateFeatureForWindow(singleNoAugData[:, 0:constants.samplesPerWindow])
        lastNoAugFeature = calculateFeatureForWindow(
            singleNoAugData[:, constants.windowShift:constants.windowShift+constants.samplesPerWindow])
        currentIndex = constants.windowShift*2


        while (currentIndex + constants.samplesPerWindow <= len(singleNoAugData[0])
               & len(singleNoAugData[0]) >= constants.samplesPerWindow):

            currentNonAugFeature = calculateFeatureForWindow(
                singleNoAugData[:, currentIndex:currentIndex + constants.samplesPerWindow])
            featureNoAugVector = currentNonAugFeature.tolist()
            featureNoAugVector.extend(copy.deepcopy(nonAugFeatureBeforeLast))
            featureNoAugVector.extend(copy.deepcopy(lastNoAugFeature))

            nonAugFeatureBeforeLast = copy.deepcopy(lastNoAugFeature)
            lastNoAugFeature = copy.deepcopy(currentNonAugFeature)
            X_train.append(np.asarray(featureNoAugVector))
            y_train.append("no augmentation")
            currentIndex += constants.windowShift

        index += 2

    return X_train, y_train