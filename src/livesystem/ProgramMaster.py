import sys
import copy
import pylsl
import threading
from collections import deque
import livesystem.MidiManager as midimanager
import livesystem.LiveSystemManager as live
import livesystem.CalibrationManager as calibration
import livesystem.gui.GuiController as guiController

class ProgramMaster:

    def __init__(self):
        self.streamInlet: pylsl.StreamInlet

        self.calibrationSem = threading.Semaphore()
        self.calibrationOn  = False
        self.calibrationThread: threading.Thread

        #liveSystem is referring to the situation after the calibration is completed
        #and the modulation can be used to trigger the sound modulation
        self.liveSystemSem = threading.Semaphore()
        self.inLiveSystem  = False
        self.liveSystemThread: threading.Thread

        self.midiManager        = midimanager.MidiManager(self)
        self.guiController      = guiController.guiController(self)
        self.calibrationManager = calibration.calibrationManager(self)
        self.liveSystemManager: live.LiveSystemManager


        self.predictionSem       = threading.Semaphore()
        self.currentlyAugmenting = False
        self.lastTwoPredictions  = deque([False, False])  #False: no augmentation; True: augmentation
        self.midiEffectOn        = False
        self.midiEffectThread    = threading.Thread(target=self.midiManager.sendEffect)
        self.midiThread: threading.Thread

        self.offlineSystemData = []
        self.modOnTimestamp    = -1
        self.modsTimestamp     = []     #saves all the timestamp pairs of the modulations: [(begin, end), ...]
        self.programPaused     = False



    #run gui for the live-system
    def startWindow(self):
        self.guiController.launchWindow()


    # getter
    def getCalibrationOn(self):
        self.calibrationSem.acquire()
        res = copy.deepcopy(self.calibrationOn)
        self.calibrationSem.release()
        return res

    def getTestSystemOn(self):
        self.liveSystemSem.acquire()
        res = copy.deepcopy(self.inLiveSystem)
        self.liveSystemSem.release()
        return res

    def getCurrentPrediction(self):
        self.predictionSem.acquire()
        res = copy.deepcopy(self.currentlyAugmenting)
        self.predictionSem.release()
        return res


    # setter
    def setCalibrationOn(self, bool):
        self.calibrationSem.acquire()
        self.calibrationOn = bool
        self.calibrationSem.release()


    def setTestSystemOn(self, bool):
        self.liveSystemSem.acquire()
        self.inLiveSystem = bool
        self.liveSystemSem.release()


    def setCurrentPrediction(self, augmentationOn):
        if augmentationOn and not self.midiEffectThread.isAlive():
            print("augmentation started")
            self.startMidiEffect()

        elif not augmentationOn and self.midiEffectThread.isAlive():
            print("augmentation ended")
            self.endMidiEffect()

        self.predictionSem.acquire()
        self.lastTwoPredictions.popleft()
        self.lastTwoPredictions.append(augmentationOn)
        self.predictionSem.release()


    def startMidiEffect(self):
        self.midiEffectOn = True
        self.midiEffectThread = threading.Thread(target=self.midiManager.sendEffect)
        self.midiEffectThread.start()

    def endMidiEffect(self):
        self.midiEffectOn = False
        self.midiEffectThread.join()


    def connectToLSLStream(self, connectionType="type", connectionVal="EEG"):
        streams = pylsl.resolve_stream(connectionType, connectionVal)
        # create a new inlet to read from the stream
        self.streamInlet = pylsl.StreamInlet(streams[0])


    def startCalibration(self):
        self.setCalibrationOn(True)
        self.calibrationThread = threading.Thread(target=self.calibrationManager.startCalibration,
                                                  args=(self.streamInlet,))
        self.calibrationThread.start()


    def startMod(self):
        self.modOnTimestamp = pylsl.local_clock()
        print("modon: ", self.modOnTimestamp)

        if self.inLiveSystem:
            self.startMidiEffect()

    def endMod(self):
        self.modsTimestamp.append((self.modOnTimestamp, pylsl.local_clock()))
        print("mods: ", self.modsTimestamp)

        if self.inLiveSystem:
            self.endMidiEffect()


    def endCalibration(self):
        self.setCalibrationOn(False)
        self.calibrationThread.join()

        self.calibrationManager.startTraining()
        self.modsTimestamp = []
        self.modOnTimestamp = -1
        self.programPaused = True
        threading.Thread(target=self.keepPullingSamplesFromInlet).start()

    def keepPullingSamplesFromInlet(self):
        while self.programPaused:
            self.streamInlet.pull_sample()


    def startLiveSystem(self):
        print("starting the system; this is the timestamp: ", pylsl.local_clock())
        self.setTestSystemOn(True)
        self.modsTimestamp  = []
        self.modOnTimestamp = -1

        if not self.calibrationManager.svm:
            print("ERROR: Program-Manager: YOU CANNOT START the system WITHOUT calibration!")
            return

        self.liveSystemManager = live.LiveSystemManager(self, self.calibrationManager.svm)
        self.programPaused  = False
        self.liveSystemThread  = threading.Thread(target=self.liveSystemManager.startSystem,
                                                  args=(self.streamInlet,))
        self.liveSystemThread.start()


    def stopSystem(self, livesysturn):
        print("stopping the system: timestamp: ", pylsl.local_clock())
        self.setTestSystemOn(False)
        self.liveSystemManager.stopSystem(livesysturn)
        self.liveSystemThread.join()
        self.programPaused = True
        threading.Thread(target=self.keepPullingSamplesFromInlet).start()


    def quit(self):
        self.programPaused = False
        sys.exit()


def main():
    programMaster = ProgramMaster()
    programMaster.startWindow()

