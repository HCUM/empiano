import mne
import logging
import datetime
import numpy as np
from joblib import dump
from sklearn import svm
from plotter import dataPlotter
import storage.constants as constants
from workers import preprocessor, csvWriter
import workers.MLDataManager as mlDataManager
import workers.recordingsManager as recordmanager
from sklearn.model_selection import cross_val_score, ShuffleSplit


class calibrationManager:
    def __init__(self, liveSysManager):
        self.logger = logging.getLogger()
        self.liveSysManager = liveSysManager
        self.resavedStreamData = [[] for i in range(constants.numberOfChannels)]
        self.streamData = []
        self.mods = []
        self.eegStreamTimeOffset = -1
        self.svm: svm.SVC
        #self.logger.info("Calibration-Manager: Initialized")

    def startCalibration(self, inlet):
        #self.logger.info("Calibration-Manager: Started")
        self.eegStreamTimeOffset = inlet.time_correction()
        csvWriter.timestampToCsv(self.eegStreamTimeOffset)
        self.logger.info("Calibration-Manager: eeg time correction: %s", self.eegStreamTimeOffset)
        #while len(self.streamData)<111940:
        while self.liveSysManager.getCalibrationOn():
            self.saveSample(inlet.pull_sample())

    def saveSample(self, sample):
        #print("sample received: ", sample)
        #self.logger.info("Calibration-Manager: Sample received: %s", sample)
        (data, timestamp) = sample
        #print("timestamp received: ", timestamp)
        #TODO had to adjust the following line
        self.streamData.append((np.asarray(data) * 0.000001, timestamp+self.eegStreamTimeOffset))
        #self.streamData.append((np.asarray(data), timestamp))
        #print("local timestamp: ", pylsl.local_clock())
        #self.logger.info("Calibration-Manager: Sample being saved to data: %s", data)


    def prepareData(self):
        #dataPlotter.plotDataWithTimestamps(self.streamData, self.liveSysManager.modsTimestamp)

        for (modon, modoff) in self.liveSysManager.modsTimestamp:
            matchesOn = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp >= modon]
            #self.logger.info("Calibration-Manager: matches on: %s", matchesOn)

            matchesOff = [tmstmp for (smp, tmstmp) in self.streamData if tmstmp <= modoff]
            #self.logger.info("Calibration-Manager: matches off: %s", matchesOff)
            #this is needed because the calibration end with a mod-phase.
            #so in case,
            if not matchesOff:
                (sam, time) = self.streamData[-1]
                matchesOff.append(time)

            self.mods.append((len(self.streamData)-len(matchesOn), len(matchesOff)-1))


        for (sample, timestamp) in self.streamData:
            for i in range(len(self.resavedStreamData)):
                self.resavedStreamData[i].append(sample[i])
        #self.logger.info("Calibration-Manager: stream data: %s", self.streamData)
        #self.logger.info("Calibration-Manager: cali data: %s", self.resavedStreamData)



    def startTraining(self):
        csvWriter.dataPlusTimestampsToCsv(self.streamData, "calibration")
        csvWriter.timestampMarkerToCsv(self.liveSysManager.modsTimestamp, "calibration")

        #print("in the start training method")
        self.prepareData()
        #print("MODS NEW: ", self.mods)
        #TODO commented for study
        #csvWriter.wholeDataToCsv(self.resavedStreamData)
        #csvWriter.markerToCsv(self.mods)
        #self.logger.info("Calibration-Manager: Plotting the CaliData")
        #dataPlotter.plotCaliData(self.resavedStreamData, self.mods)
        #self.logger.info("Calibration-Manager: Starting the Training")
        #augData, nonAugData = mlDataManager.splitRecordedSample(self.resavedStreamData, self.mods, fromCali=True)
        #csvWriter.dataToCsv(augData, nonAugData)
        preprocessedStreamData = preprocessor.performPreprocessing(self.resavedStreamData)
        #self.logger.info("Calibration-Manager: Data after preprocessing: %s", self.caliData)
        #TODO changed the line below to the line below that line -> fromCali = False, so nothing is being cutted off
        #augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods, fromCali=True)
        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedStreamData, self.mods, fromCali=False)
        X_train, _, y_train, _, ratioAugSamples, _ = mlDataManager.createMLData(augData, nonAugData,
                                                                             wholeSplit=False, noSplit=True)
        self.trainSVM(X_train, y_train)
        #self.logger.info("Calibration-Manager: Finished the Training")
        return augData, nonAugData, X_train, y_train


    def trainSVM(self, X_train, y_train):
        self.svm = svm.SVC()
        cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
        scores = cross_val_score(self.svm, X_train, y_train, cv=cv)
        self.logger.info("Calibration-Manager: cross-validation scores: %s", scores)
        self.svm.fit(X_train, y_train)
        #TODO adjusted for study
        now = datetime.datetime.now()
        dump(self.svm, constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_")+ 'svm.joblib')

    def offlineCali(self):
        self.logger.info("Calibration-Manager: starting the offline calibration")
        path = "./recordings/testCalibration"
        start, end, mods, startNormal, endNormal, modsNormal = recordmanager.getAllMarkers(path)
        rawData = mne.io.read_raw_brainvision(path + ".vhdr", montage=None, misc='auto', scale=1.0,
                                              preload=True, verbose=True)
        rawRealData = rawData._data[constants.lowestValidChannel:constants.highestValidChannel + 1,
                      start:end]  # trim data to the start and end markers and to only the 8 channels that have been used
        preprocessedData = preprocessor.performPreprocessing(rawRealData)
        dataPlotter.plotCaliData(preprocessedData, mods)

        self.liveSysManager.offlineSystemData = \
            rawData._data[constants.lowestValidChannel:constants.highestValidChannel + 1, startNormal:endNormal]

        #import plotter.fftPlotter
        #plotter.fftPlotter.plotFFT(preprocessedData)
        #need to cut data because I had 10 seconds break between every part
        augData, nonAugData = mlDataManager.splitRecordedSample(preprocessedData, mods, fromCali=True)
        x_train, _, y_train, _, _ = mlDataManager.createMLData(augData, nonAugData, wholeSplit=False)
        self.trainSVM(x_train, y_train)
        self.logger.info("Calibration-Manager: Ended the offline calibration and successfully trained the SVM")
