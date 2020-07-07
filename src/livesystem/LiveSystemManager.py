import copy
import logging
import threading
import numpy as np
from collections import deque
from plotter import dataPlotter
import storage.Constants as constants
from workers import Preprocessor, FeatureCalculator, CSVWriter

class LiveSystemManager:

    def __init__(self, programMaster, svm):
        self.logger = logging.getLogger()
        self.svm = svm
        self.samplesToNextPrediction = constants.samplesPerWindow
        self.bufferSize = constants.samplesPerWindow * 10
        self.programMaster = programMaster
        self.predictionThread: threading.Thread
        self.ringBuffer = deque([[0.0 for j in range(constants.numberOfChannels)] for i in range(self.bufferSize)])
        #self.logger.info("Test-Sys-Manager: Initialized")
        self.plotter = dataPlotter.LivePlotter()
        self.streamData = []
        self.eegStreamTimeOffset = -1
        self.lastFeature = []
        self.secondToLastFeature = []



    def startSystem(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()
        #self.logger.info("Test-Sys-Manager: Started")
        while(self.programMaster.getTestSystemOn()):
            self.saveSampleToRingbuffer(inlet.pull_sample())
            #self.logger.info("Test-Sys-Manager: current last element Ringbuffer: %s", self.ringBuffer[-1])

            if self.samplesToNextPrediction == 0:
                deepCopyRingBuffer = copy.deepcopy(self.ringBuffer)
                threading.Thread(target=self.performPrediction, args=(deepCopyRingBuffer,)).start()
                self.samplesToNextPrediction = constants.windowShift
            self.samplesToNextPrediction -= 1


    def saveSampleToRingbuffer(self, sample):
        (data, timestamp) = sample

        self.streamData.append((np.asarray(data) * 0.000001, timestamp + self.eegStreamTimeOffset))

        #self.logger.info("Test-Sys-Manager: sample received: %s", sample)
        #remove the last element
        self.ringBuffer.popleft()
        #add the latest
        usefulSample = self.makeSampleUseful(sample)
        self.ringBuffer.append(usefulSample)
        self.plotter.addSample(usefulSample)

    def makeSampleUseful(self, sample):
        try:
            (data, _) = sample
        except:
            data = sample
        data = np.asarray(data)
        data = data*0.000001
        return data[:constants.numberOfChannels]

    def performPrediction(self, ringBuffer):
        eegDf = [[] for i in range(constants.numberOfChannels)]

        for sample in list(ringBuffer):
            for j in range(len(sample)):
                eegDf[j].append(sample[j])
        #self.logger.info("Test-Sys-Manager: Ring buffer: %s", ringBuffer)
        #self.logger.info("Test-Sys-Manager: Resaved data: %s", eegDf)

        #preprocess data
        eegDf = Preprocessor.performPreprocessing(eegDf)
        #self.logger.info("Test-Sys-Manager: Data after preprocessing: %s", eegDf)

        eegDf     = np.asarray(eegDf)
        lastIndex = len(eegDf[0])
        #self.logger.info("Test-Sys-Manager: "
        #                 "Data performing the feature calculation on: %s",
        #                 eegDf[:, (lastIndex-constants.samplesPerWindow):lastIndex])
        feature = FeatureCalculator.calculateFeatureForWindow(eegDf[:, (lastIndex - constants.samplesPerWindow):lastIndex])
        #self.logger.info("Test-Sys-Manager: calculated feature: %s", feature)

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

    def stopSystem(self, livesysturn):
        CSVWriter.dataPlusTimestampsToCsv(self.streamData, "livesystemRound" + str(livesysturn))
        CSVWriter.timestampMarkerToCsv(self.programMaster.modsTimestamp, "livesystemRound" + str(livesysturn))
        #self.plotter.finishPlot()