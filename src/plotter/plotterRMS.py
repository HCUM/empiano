import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

import storage.constants as constants
import workers.featureCalc as feature

xVals = []
yVals = []
augmentationMarkers = []


def plotData(eegData, mods, title):
    global yVals
    yVals = [[] for i in range(constants.numberOfChannels)]
    eegData = np.asarray(eegData)
    addData(eegData[:, :mods[0][0]])
    for i in range(len(mods)):
        addData(eegData[:, mods[i][0]:mods[i][1]], True)
        if i + 1 == len(mods):
            addData(eegData[:, mods[i][1]:])
        else:
            addData(eegData[:, mods[i][1]:mods[i + 1][0]])

    showPlot(title)


def addData(data, augmented=False):
    global yVals, augmentationMarkers
    i = 0
    if augmented: augmentationMarkers.append(len(yVals[0]))
    while (i + constants.samplesPerWindow < len(data[0])):
        rmsVals = feature.calculateFeatureForWindow(data[:, i:i + constants.samplesPerWindow], False)
        for j in range(len(rmsVals)):
            yVals[j].append(rmsVals[j])
        i += constants.windowShift
    # add end of augmentation marker as well
    if augmented: augmentationMarkers.append(len(yVals[0]) - 1)


def addY(y):
    for i in range(len(y)):
        yVals[i].append(y[i])


def showPlot(title):
    global xVals
    xVals = range(len(yVals[0]))
    for i in range(len(yVals)):
        plt.plot(xVals, yVals[i], label="channel" + str(i))
    for j in range(len(augmentationMarkers)):
        plt.axvline(x=augmentationMarkers[j])
    plt.legend(loc='best')
    savePlot("./plots/rmsPlots/" + getPlotTitle(title) + ".png")
    plt.show()


def savePlot(path):
    plt.savefig(path)


def getPlotTitle(plotTitle):
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H.%M.%S_") + plotTitle
