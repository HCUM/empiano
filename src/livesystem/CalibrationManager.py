import datetime
import numpy as np
from joblib import dump
from sklearn import svm
import storage.Constants as constants
from helpers import Preprocessor, CSVWriter
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
        CSVWriter.timestampToCsv(self.eegStreamTimeOffset)

        while self.programMaster.getCalibrationOn():
            self.saveSample(inlet.pull_sample())


    def saveSample(self, sample):
        (data, timestamp) = sample
        #TODO had to adjust the following line
        self.streamData.append((np.asarray(data) * 0.000001, timestamp+self.eegStreamTimeOffset))


    def prepareData(self):
        #dataPlotter.plotDataWithTimestamps(self.streamData, self.liveSysManager.modsTimestamp)

        for (modon, modoff) in self.programMaster.modsTimestamp:
            matchesOn = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp >= modon]

            matchesOff = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp <= modoff]
            #this is needed because the calibration end with a mod-phase.
            #so in case,
            if not matchesOff:
                (sam, time) = self.streamData[-1]
                matchesOff.append(time)

            self.mods.append((len(self.streamData)-len(matchesOn), len(matchesOff)-1))


        for (sample, timestamp) in self.streamData:
            for i in range(len(self.resavedStreamData)):
                self.resavedStreamData[i].append(sample[i])



    def startTraining(self):
        CSVWriter.dataPlusTimestampsToCsv(self.streamData, "calibration")
        CSVWriter.timestampMarkerToCsv(self.programMaster.modsTimestamp, "calibration")

        self.prepareData()
        #print("MODS NEW: ", self.mods)
        #TODO commented for study
        #csvWriter.wholeDataToCsv(self.resavedStreamData)
        #csvWriter.markerToCsv(self.mods)

        #dataPlotter.plotCaliData(self.resavedStreamData, self.mods)

        #augData, nonAugData = mlDataManager.splitRecordedSample(self.resavedStreamData, self.mods, fromCali=True)
        #csvWriter.dataToCsv(augData, nonAugData)
        preprocessedStreamData = Preprocessor.performPreprocessing(self.resavedStreamData)

        #TODO changed the line below to the line below that line -> fromCali = False, so nothing is being cutted off
        #augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods, fromCali=True)
        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods, fromCali=False)
        X_train, _, y_train, _, ratioAugSamples, _ = mlDataManager.createMLData(augData, nonAugData,
                                                                             wholeSplit=False, noSplit=True)
        self.trainSVM(X_train, y_train)

        return augData, nonAugData, X_train, y_train


    def trainSVM(self, X_train, y_train):
        self.svm = svm.SVC()
        cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
        scores = cross_val_score(self.svm, X_train, y_train, cv=cv)

        self.svm.fit(X_train, y_train)
        #TODO adjusted for study
        now = datetime.datetime.now()
        dump(self.svm, constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_")+ 'svm.joblib')