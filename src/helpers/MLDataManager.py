import copy
import numpy as np
from storage import Constants as constants
from helpers.FeatureCalculator import calculateFeatureForWindow


'''
This method is used for splitting the eegData into augmented and not augmented data
the splitted and returned data will have the following type:
   [
    [ [data_channel_1_aug_1][data_channel_2_aug_1] ... [data_channel_8_aug_1] ]
       ...
    [[data_channel_1_last_aug][data_channel_2_last_aug] ... [data_channel_8_last_aug] ]
   ]
'''
def splitRecordedSample(eegData, mods):
    splittedAugData     = []
    splittedNonAugData  = []

    for mod in mods:
        oneAugPart  = []
        for channel in eegData:
            oneAugPart.append(np.array(channel[mod[0]: mod[1]]))
        splittedAugData.append(oneAugPart)

    smallestNonAugIndex = 0
    eegData = np.asarray(eegData)
    for mod in mods:
        slice = eegData[:,smallestNonAugIndex:mod[0]]
        splittedNonAugData.append(slice)
        smallestNonAugIndex = mod[1]

    if smallestNonAugIndex < len(eegData[0]):
        slice = eegData[:,smallestNonAugIndex:]
        splittedNonAugData.append(slice)

    return splittedAugData, splittedNonAugData


'''
method is used to create the data which should be used to train the SVM
param: augData    = storing the augmented data [[channels, data]]
        nonAugData = storing the dat representing no augmentation [channels, data]
'''
def createMLData(augData, nonAugData,  wholeSplit=False,noSplit=False):
    X_train = []  #(n_samples, n_features)
    y_train = []  #(n_samples)->holding the lables/targets/classes
    X_test  = []
    y_test  = []
    X_trainIndices = []

    #create feature vectors for augmented data
    index = 2
    for i in range(len(augData)):
        singleAugData = np.asarray(augData[i])
        lastFeature = calculateFeatureForWindow(singleAugData[:, 0:constants.samplesPerWindow])
        secondToLastFeature = calculateFeatureForWindow(
            singleAugData[:, constants.windowShift:constants.windowShift+constants.samplesPerWindow])

        j = constants.windowShift *2
        augFeaturesCsv = []
        while (j + constants.samplesPerWindow <= len(singleAugData[0]) &
               len(singleAugData[0]) >= constants.samplesPerWindow):

            currentFeature = calculateFeatureForWindow(singleAugData[:, j:j + constants.samplesPerWindow])
            augFeaturesCsv.append(currentFeature)
            featureVec = currentFeature.tolist()
            featureVec.extend(copy.deepcopy(lastFeature))
            featureVec.extend(copy.deepcopy(secondToLastFeature))
            secondToLastFeature = copy.deepcopy(lastFeature)
            lastFeature = copy.deepcopy(currentFeature)
            X_train.append(np.asarray(featureVec))
            y_train.append("augmentation")
            X_trainIndices.append(index)
            j+= constants.windowShift

        index += 2
        #csvWriter.featuresToCsv(augNames[i], augFeaturesCsv)

    amtAugTrainSamples = len(X_train)
    amtAugTestSamples = len(X_test)

    #create feature vectors for not augmented data
    index = 1
    for k in range(len(nonAugData)):
        array = nonAugData[k]
        lastNonAugFeature = calculateFeatureForWindow(array[:, 0:constants.samplesPerWindow])
        secondToLastNonAugFeature = calculateFeatureForWindow(array[:, constants.windowShift:constants.windowShift+constants.samplesPerWindow])
        currentIndex = constants.windowShift*2


        featuresCsv = []

        while (currentIndex + constants.samplesPerWindow <= len(array[0]) & len(array[0]) >= constants.samplesPerWindow):

            currentNonAugFeature = calculateFeatureForWindow(
                array[:, currentIndex:currentIndex + constants.samplesPerWindow])
            featuresCsv.append(currentNonAugFeature)
            featureNonAugVec = currentNonAugFeature.tolist()
            featureNonAugVec.extend(copy.deepcopy(lastNonAugFeature))
            featureNonAugVec.extend(copy.deepcopy(secondToLastNonAugFeature))
            secondToLastNonAugFeature = copy.deepcopy(lastNonAugFeature)
            lastNonAugFeature = copy.deepcopy(currentNonAugFeature)
            X_train.append(np.asarray(featureNonAugVec))
            y_train.append("no augmentation")
            X_trainIndices.append(index)
            currentIndex += constants.windowShift

        index += 2


    ratioAugSamples = amtAugTrainSamples / len(X_train)

    return X_train, X_test, y_train, y_test, ratioAugSamples, X_trainIndices