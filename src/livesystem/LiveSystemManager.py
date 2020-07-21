import copy
import threading
import numpy as np
from collections import deque
import storage.Constants as constants
from helpers import Preprocessor, FeatureCalculator

class LiveSystemManager:

    def __init__(self, programMaster, svm):
        self.svm = svm
        self.samplesToNextPrediction = constants.samplesPerWindow
        self.bufferSize = constants.samplesPerWindow * 10
        self.programMaster = programMaster
        self.predictionThread: threading.Thread
        self.ringBuffer = deque([[0.0 for j in range(constants.numberOfChannels)] for i in range(self.bufferSize)])
        self.streamData = []
        self.eegStreamTimeOffset = -1
        self.lastFeature = []
        self.secondToLastFeature = []


    def startSystem(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()

        while(self.programMaster.getTestSystemOn()):
            self.saveSampleToRingbuffer(inlet.pull_sample())

            if self.samplesToNextPrediction == 0:
                deepCopyRingBuffer = copy.deepcopy(self.ringBuffer)
                threading.Thread(target=self.performPrediction, args=(deepCopyRingBuffer,)).start()
                self.samplesToNextPrediction = constants.windowShift
            self.samplesToNextPrediction -= 1


    def saveSampleToRingbuffer(self, sample):
        (data, timestamp) = sample

        self.streamData.append((self.makeSampleDataUseful(data, onlyChannels=False),
                                timestamp + self.eegStreamTimeOffset))

        #remove the last element
        self.ringBuffer.popleft()
        #add the latest
        usefulSample = self.makeSampleDataUseful(data)
        self.ringBuffer.append(usefulSample)


    def makeSampleDataUseful(self, dataFromSample, onlyChannels=True):
        data = np.asarray(dataFromSample)
        data = data * constants.dataSampleCorrection
        if onlyChannels:
            return data[:constants.numberOfChannels]
        else:
            return data


    def performPrediction(self, ringBuffer):
        eegDf = [[] for i in range(constants.numberOfChannels)]

        for sample in list(ringBuffer):
            for j in range(len(sample)):
                eegDf[j].append(sample[j])

        #preprocess data
        eegDf = Preprocessor.performPreprocessing(eegDf)

        eegDf     = np.asarray(eegDf)
        lastIndex = len(eegDf[0])
        feature = FeatureCalculator.calculateFeatureForWindow(
            eegDf[:, (lastIndex - constants.samplesPerWindow):lastIndex])

        if len(self.lastFeature) != 0 and len(self.secondToLastFeature) != 0:
            featureVec = feature.tolist()
            featureVec.extend(copy.deepcopy(self.lastFeature))
            featureVec.extend(copy.deepcopy(self.secondToLastFeature))
            featureVec = [featureVec]

            #set the new prediction
            prediction = self.svm.predict(featureVec)
            self.programMaster.setCurrentPrediction(prediction == "augmentation")

        self.secondToLastFeature = copy.deepcopy(self.lastFeature)
        self.lastFeature         = copy.deepcopy(feature)