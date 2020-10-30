import copy
import pylsl
import threading
import numpy as np
from pubsub import pub
from collections import deque
import storage.Constants as Constants
from helpers import Preprocessor, FeatureCalculator


###########################################################################
# Class LiveSystemManager
# -> manages the live-system
###########################################################################
class LiveSystemManager:

    def __init__(self, programMaster, svm):
        self.svm = svm
        self.samplesToNextPrediction = Constants.samplesPerWindow
        self.bufferSize = Constants.samplesPerWindow * 10
        self.programMaster = programMaster
        self.predictionThread = None
        self.ringBuffer = deque([[0.0 for j in range(Constants.numberOfChannels)] for i in range(self.bufferSize)])
        self.streamData = []
        self.eegStreamTimeOffset = -1
        self.lastFeature = []
        self.secondToLastFeature = []

    # Pulls samples from the LSL-stream and saves it to the ringbuffer;
    # once there are enough samples for a prediction, it calls the prediction method
    def startSystem(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()

        while self.programMaster.getLiveSystemOn():
            self.saveSampleToRingbuffer(inlet.pull_sample())

            if self.samplesToNextPrediction == 0:
                deepCopyRingBuffer = copy.deepcopy(self.ringBuffer)
                threading.Thread(target=self.performPrediction, args=(deepCopyRingBuffer,)).start()
                self.samplesToNextPrediction = Constants.windowShift
            self.samplesToNextPrediction -= 1

    # Saves the received sample to the ringbuffer
    # after correcting the timestamp and its format
    def saveSampleToRingbuffer(self, sample):
        (data, timestamp) = sample

        self.streamData.append((self.makeSampleDataUseful(data, onlyChannels=False),
                                timestamp + self.eegStreamTimeOffset))

        # remove the last element
        self.ringBuffer.popleft()
        # add the latest
        usefulSample = self.makeSampleDataUseful(data)
        self.ringBuffer.append(usefulSample)
        #self.programMaster.tmstmpLastSample = pylsl.local_clock()
        self.programMaster.setLastSampleTimestamp(pylsl.local_clock())

    # Returns only the necessary data portion of a sample
    @staticmethod
    def makeSampleDataUseful(dataFromSample, onlyChannels=True):
        data = np.asarray(dataFromSample)
        data = data * Constants.dataSampleCorrection
        if onlyChannels:
            return data[:Constants.numberOfChannels]
        else:
            return data

    # First reformats the data ([ [data channel 1][data channel 2]...[data channel n] ]),
    # calls preprocessing, feature calculation, SVM prediction
    def performPrediction(self, ringBuffer):
        emgDf = [[] for i in range(Constants.numberOfChannels)]

        for sample in list(ringBuffer):
            for j in range(len(sample)):
                emgDf[j].append(sample[j])

        # preprocess data
        emgDf = Preprocessor.performPreprocessing(emgDf)

        emgDf = np.asarray(emgDf)
        lastIndex = len(emgDf[0])
        feature = FeatureCalculator.calculateFeatureForWindow(
            emgDf[:, (lastIndex - Constants.samplesPerWindow):lastIndex])

        if len(self.lastFeature) != 0 and len(self.secondToLastFeature) != 0:
            featureVec = feature.tolist()
            featureVec.extend(copy.deepcopy(self.lastFeature))
            featureVec.extend(copy.deepcopy(self.secondToLastFeature))
            featureVec = [featureVec]

            # set the new prediction
            newPrediction = self.svm.predict(featureVec)
            oldPrediction = self.programMaster.lastTwoPredictions[1]
            boolPrediction = (newPrediction[0] == "augmentation")
            self.programMaster.setCurrentPrediction(boolPrediction)
            #self.programMaster.tmstmpLastPrediction = pylsl.local_clock()
            if boolPrediction != oldPrediction:
                pub.sendMessage("liveSystemPanelListener", msg="PREDICTION_CHANGED", arg=newPrediction)

        self.secondToLastFeature = copy.deepcopy(self.lastFeature)
        self.lastFeature = copy.deepcopy(feature)
