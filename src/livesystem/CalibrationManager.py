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
        self.resavedStreamData = [[] for _ in range(Constants.numberOfChannels)]
        self.streamData = []
        self.mods = []
        self.eegStreamTimeOffset = -1
        self.svm = None
        self.crossValScores = []

    # starts to pull and save the data from the incoming LSL-stream
    # input stream of the form: (rowid, inlet, time_correction)
    def startCalibration(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()

        while self.programMaster.getCalibrationOn():
            self.saveSample(inlet.pull_sample())

    # saves the received sample after correcting its timestamp
    def saveSample(self, sample):
        (data, timestamp) = sample
        self.streamData.append(
            (np.asarray(data) * Constants.dataSampleCorrection, timestamp + self.eegStreamTimeOffset))

    # Calculates the corresponding indices for the timestamps marking modulation on and off
    # Resaves the stream data, so it matches [ [data channel 1][data channel 2]...[data channel n] ]
    def prepareData(self):
        for (modon, modoff) in self.programMaster.modsTimestamp:
            matchesOn = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp >= modon]

            matchesOff = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp <= modoff]

            if not matchesOff:
                (sam, time) = self.streamData[-1]
                matchesOff.append(time)

            self.mods.append((len(self.streamData) - len(matchesOn), len(matchesOff) - 1))

        for (sample, timestamp) in self.streamData:
            for i in range(Constants.numberOfChannels):
                self.resavedStreamData[i].append(sample[i])

    # Calls all the functions needed for training the SVM:
    # data preparation, preprocessing, splitting the data, feature calculation
    def startTraining(self):
        self.prepareData()

        preprocessedStreamData = Preprocessor.performPreprocessing(self.resavedStreamData)

        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods)
        X_train, y_train = mlDataManager.createMLData(augData, nonAugData)
        self.trainSVM(X_train, y_train)

        return augData, nonAugData, X_train, y_train

    # Performs a 10-fold cross validation and trains the SVM
    def trainSVM(self, X_train, y_train):
        self.svm = svm.SVC()
        cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)
        self.crossValScores = cross_val_score(self.svm, X_train, y_train, cv=cv)
        pub.sendMessage("liveSystemPanelListener", msg="CROSS_VAL_SET", arg=self.crossValScores.round(2))
        self.svm.fit(X_train, y_train)
