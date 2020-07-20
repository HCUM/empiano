import datetime
import numpy as np
from joblib import dump
from sklearn import svm
from helpers import Preprocessor
import storage.Constants as constants
import helpers.MLDataManager as mlDataManager
from sklearn.model_selection import cross_val_score, ShuffleSplit


class calibrationManager:
    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.resavedStreamData = [[] for _ in range(constants.numberOfChannels)]
        self.streamData = []
        self.mods = []
        self.eegStreamTimeOffset = -1
        self.svm: svm.SVC


    def startCalibration(self, inlet):
        self.eegStreamTimeOffset = inlet.time_correction()

        while self.programMaster.getCalibrationOn():
            self.saveSample(inlet.pull_sample())


    def saveSample(self, sample):
        (data, timestamp) = sample
        self.streamData.append((np.asarray(data) * constants.dataSampleCorrection, timestamp+self.eegStreamTimeOffset))


    def prepareData(self):
        for (modon, modoff) in self.programMaster.modsTimestamp:
            matchesOn = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp >= modon]

            matchesOff = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp <= modoff]

            if not matchesOff:
                (sam, time) = self.streamData[-1]
                matchesOff.append(time)

            self.mods.append((len(self.streamData)-len(matchesOn), len(matchesOff)-1))

        for (sample, timestamp) in self.streamData:
            for i in range(constants.numberOfChannels):
                self.resavedStreamData[i].append(sample[i])



    def startTraining(self):
        self.prepareData()

        preprocessedStreamData = Preprocessor.performPreprocessing(self.resavedStreamData)

        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods)
        X_train, y_train = mlDataManager.createMLData(augData, nonAugData)
        self.trainSVM(X_train, y_train)

        return augData, nonAugData, X_train, y_train


    def trainSVM(self, X_train, y_train):
        self.svm = svm.SVC()
        cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
        scores = cross_val_score(self.svm, X_train, y_train, cv=cv)
        self.svm.fit(X_train, y_train)