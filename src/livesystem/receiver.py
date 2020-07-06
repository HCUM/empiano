from pylsl import StreamInlet, resolve_stream

import storage.constants as constants
from sklearn import svm
from sklearn import tree
from sklearn.metrics import accuracy_score
import workers.featureCalc as featureCalc
import pygame.midi

list    = list()
svmClf  = svm.SVC()
treeClf = tree.DecisionTreeClassifier()

def receiveData():
    streams = resolve_stream('name', 'EMG-data')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample = inlet.pull_sample()
        saveSample(sample)
        print(sample)

def saveSample(sample):
    global list
    if len(list) == constants.samplesPerWindow:
        handlePrediction(list)
    list.append(sample)

def handlePrediction(list):
    windowData     = translateListToNormalDataShape(list)
    feature        = featureCalc.calculateFeatureForWindow(windowData)
    svmPrediction  = svmClf.predict(feature)
    treePrediction = treeClf.predict(feature)
    if svmPrediction == 'augmentation':
        #do the midi stuff here
        return


def translateListToNormalDataShape(list):
    windowData = [[] for i in range(constants.highestValidChannel+1)]

    for j in range(len(list)):
        for k in range(constants.highestValidChannel+1):
            windowData[k].append(list[j][k])

    return windowData

def createClassifier(xTrain, yTrain):
    svmClf.fit(xTrain, yTrain)

    treeClf.fit(xTrain, yTrain)
