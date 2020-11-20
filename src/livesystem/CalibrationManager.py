import pylsl
import numpy as np
from pubsub import pub
from sklearn import svm
from helpers import Preprocessor
import storage.Constants as Constants
import helpers.MLDataManager as mlDataManager
from sklearn.model_selection import cross_val_score, ShuffleSplit


###########################################################################
# Class CalibrationManager
# -> manages the calibration
###########################################################################
class CalibrationManager:
    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.restoredStreamData = [[] for _ in range(Constants.numberOfChannels)]
        self.streamData = []
        self.mods = []
        self.eegStreamTimeOffset = -1
        self.svm = None
        self.crossValScores = []

    # Starts to pull and save the data from the incoming LSL-stream
    # input stream of the form: (rowid, inlet, time_correction)
    def startCalibration(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()

        while self.programMaster.getCalibrationOn():
            self.saveSample(inlet.pull_sample())

    # Saves the received sample after correcting its timestamp
    def saveSample(self, sample):
        (data, timestamp) = sample
        self.streamData.append(
            (np.asarray(data) * Constants.dataSampleCorrection, timestamp + self.eegStreamTimeOffset))
        self.programMaster.setLastSampleTimestamp(pylsl.local_clock())

    # Calculates the corresponding indices for the timestamps marking modulation on and off
    # Restores the stream data, so it matches [ [data channel 1][data channel 2]...[data channel n] ]
    def prepareData(self):
        for (modon, modoff) in self.programMaster.modsTimestamp:
            matchesOn = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp >= modon]

            matchesOff = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp <= modoff]

            if not matchesOff:
                (sam, time) = self.streamData[-1]
                matchesOff.append(time)

            self.mods.append((len(self.streamData) - len(matchesOn), len(matchesOff) - 1))
        if len(self.mods) != len(self.programMaster.modsTimestamp):
            return "Converting modulation timestamps to array indices failed."

        for (sample, timestamp) in self.streamData:
            for i in range(Constants.numberOfChannels):
                self.restoredStreamData[i].append(sample[i])
        if len(self.restoredStreamData) != Constants.numberOfChannels:
            return "Restoring the stream data failed."
        return None

    # Calls all the functions needed for training the SVM:
    # data preparation, pre-processing, splitting the data, feature calculation
    def startTraining(self):
        errorStr = self.prepareData()
        if errorStr:
            return errorStr

        preprocessedStreamData = Preprocessor.performPreprocessing(self.restoredStreamData)
        if not preprocessedStreamData:
            return "Pre-processing failed."

        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods)
        X_train, y_train = mlDataManager.createMLData(augData, nonAugData)
        return self.trainSVM(X_train, y_train)

    # Performs a 10-fold cross validation and trains the SVM
    def trainSVM(self, X_train, y_train):
        self.svm = svm.SVC()
        cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)
        self.crossValScores = cross_val_score(self.svm, X_train, y_train, cv=cv)
        pub.sendMessage("liveSystemPanelListener", msg="CROSS_VAL_SET", arg=self.crossValScores.round(2))
        try:
            self.svm.fit(X_train, y_train)
        except ValueError as e:
            return e
        except TypeError as e:
            return e
        return None


