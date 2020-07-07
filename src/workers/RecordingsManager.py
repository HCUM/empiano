import re
import mne
import storage.Constants as constants
import csv
import numpy as np

def getDataAndMarkers():
    start, end, mods, startNormal, endNormal, modsNormal = getAllMarkers(constants.recordingsPath)
    rawData = mne.io.read_raw_brainvision(constants.recordingsPath + ".vhdr", montage=None, misc='auto', scale=1.0, preload=True,
                                          verbose=True)
    rawRealData = rawData._data[constants.lowestValidChannel:constants.highestValidChannel + 1,
                  start:end]  # trim data to the start and end markers and to only the 8 channels that have been used
    testData = []
    if startNormal != -1:
        testData = rawData._data[constants.lowestValidChannel:constants.highestValidChannel + 1,
                  startNormal:endNormal]
    return rawRealData, mods, testData


#This method is used to get the marker-data out of the .vmrk-file
def getAllMarkers(pathStr):
    start, end, mods, startNormal, endNormal, modsNormal = readHeader(pathStr)
    return start, end, updateModTimes(start, mods), startNormal, endNormal, modsNormal


def readHeader(pathStr):
    file  = open(pathStr+".vmrk", "r")
    lines = file.readlines()
    file.close()

    modon  = []
    modoff = []
    modonNormal  = []
    modoffNormal = []
    start = -1
    end = -1
    startNormal = -1
    endNormal = -1
    for line in lines:
        modonNr = re.search("Mk[0-9]+=Comment,modon,(.*?),", line)
        if modonNr:
            if startNormal == -1:
                modon.append(int(modonNr.group(1)))
            else:
                modonNormal.append(int(modonNr.group(1)))
            continue
        modoffNr = re.search("Mk[0-9]+=Comment,modoff,(.*?),", line)
        if modoffNr:
            if startNormal == -1:
                modoff.append(int(modoffNr.group(1)))
            else:
                modoffNormal.append(int(modoffNr.group(1)))
            continue
        startNr  = re.search("Mk[0-9]+=Comment,start,(.*?),", line)
        if startNr:
            start = int(startNr.group(1))
            continue
        endNr    = re.search("Mk[0-9]+=Comment,end,(.*?),", line)
        if endNr:
            end = int(endNr.group(1))
            continue
        startNormalNr = re.search("Mk[0-9]+=Comment,startnormal,(.*?),", line)
        if startNormalNr:
            startNormal = int(startNormalNr.group(1))
            continue
        endNormalNr = re.search("Mk[0-9]+=Comment,endnormal,(.*?),", line)
        if endNormalNr:
            endNormal = int(endNormalNr.group(1))


    mods = []
    for i in range(len(modon)):
        mods.append([modon[i], modoff[i]])

    modsNormal = []
    for i in range(len(modonNormal)):
        modsNormal.append([modonNormal[i], modoffNormal[i]])

    if start == -1: start = 2000

    return start, end, mods, startNormal, endNormal, modsNormal


def updateModTimes(start, mods):
    newMods = []
    for [on, off] in mods:
        newMods.append([on - start, off - start])
    return newMods

def getDataAndMarkersCsv(dataPath, modsPath):
    rawData = []

    with open("./study/pilotStudy/"+dataPath+".csv") as csvFile:

        csvReader = csv.reader(csvFile, delimiter=",")
        next(csvReader, None)

        for row in csvReader:
            row = [float(value) for value in row]
            rawData.append((row[0:-1], row[-1]))

    mods = []
    with open("./study/pilotStudy/"+modsPath+".csv") as csvMarkerFile:
        csvMarkerReader = csv.reader(csvMarkerFile, delimiter=",")
        for row in csvMarkerReader:
            mods.append((float(row[0]), float(row[1])))
    return rawData, mods

