import sys
import copy
import pylsl
import threading
from pubsub import pub
from collections import deque
import storage.Constants as Constants
import livesystem.LiveSystemManager as Live
import livesystem.MidiManager as MidiManager
import livesystem.StreamManager as StreamManager
import livesystem.CalibrationManager as Calibration
import livesystem.gui.GuiController as GuiController


###########################################################################
# Class ProgramMaster
# -> everything goes through here, manages all the sub-classes
###########################################################################
class ProgramMaster:
    def __init__(self):
        self.streamManager = StreamManager.StreamManager()

        self.programPauseThread = None

        self.calibrationSem = threading.Semaphore()
        self.calibrationOn = False
        self.calibrationThread = None

        # liveSystem is referring to the situation after the calibration is completed
        # and the modulation can be used to trigger the sound modulation
        self.liveSystemSem = threading.Semaphore()
        self.inLiveSystem = False
        self.liveSystemThread = None
        self.firstLiveRoundDone = False

        self.midiManager = MidiManager.MidiManager(self)
        self.guiController = GuiController.guiController(self)
        self.calibrationManager = None
        self.liveSystemManager = None

        self.predictionSem = threading.Semaphore()
        self.lastTwoPredictions = deque([False, False])  # False: no augmentation; True: augmentation
        self.midiEffectOn = False
        self.midiEffectThread = threading.Thread(target=self.midiManager.sendEffect)
        self.midiThread = None

        self.modOnTimestamp = -1
        self.modsTimestamp = []  # saves all the timestamp pairs of the modulations: [(begin, end), ...]
        self.programPaused = False

    # run gui for the live-system
    def startWindow(self):
        self.guiController.launchWindow()

    # getters with semaphore

    def getCalibrationOn(self):
        self.calibrationSem.acquire()
        res = copy.deepcopy(self.calibrationOn)
        self.calibrationSem.release()
        return res

    def getLiveSystemOn(self):
        self.liveSystemSem.acquire()
        res = copy.deepcopy(self.inLiveSystem)
        self.liveSystemSem.release()
        return res

    # setters with semaphore

    def setCalibrationOn(self, boolean):
        self.calibrationSem.acquire()
        self.calibrationOn = boolean
        self.calibrationSem.release()

    def setInLiveSystem(self, boolean):
        self.liveSystemSem.acquire()
        self.inLiveSystem = boolean
        self.liveSystemSem.release()

    # param: augmentationOn = current prediction of the SVM whether an augmentation was performed or not;
    # starts or ends the sound effect, when needed; updates the lastTwoPredictions field
    def setCurrentPrediction(self, augmentationOn):
        if augmentationOn and not self.midiEffectThread.isAlive():
            self.startMidiEffect()

        elif not augmentationOn and self.midiEffectThread.isAlive():
            self.endMidiEffect()

        self.predictionSem.acquire()
        self.lastTwoPredictions.popleft()
        self.lastTwoPredictions.append(augmentationOn)
        self.predictionSem.release()

    def setProgramPaused(self, pause=True):
        self.programPaused = pause
        self.programPauseThread = threading.Thread(target=self.keepPullingSamplesFromInlet)
        self.programPauseThread.start()

    # updates the values changed in the settings
    @staticmethod
    def updateSettings(amtElectrodes, midiCableName, shouldCreateMidiCable):
        Constants.numberOfChannels = amtElectrodes
        Constants.virtualMIDICable = midiCableName
        Constants.createMIDICable = shouldCreateMidiCable

    # Starts the midiManager for sending the midi sound effect, in a thread
    def startMidiEffect(self):
        self.midiEffectOn = True
        self.midiEffectThread = threading.Thread(target=self.midiManager.sendEffect)
        self.midiEffectThread.start()

    # Sets the midi sound effect on false and waits for the thread handling the effect to join
    def endMidiEffect(self):
        self.midiEffectOn = False
        self.midiEffectThread.join()

    # checks whether the (in the settings) specified MIDI-cable can be found
    def checkIfMidiCableCanBeFound(self, midiCableName):
        return self.midiManager.findMidiCable(midiCableName)

    # Initializes the connection to the defined LSL-stream
    def connectToLSLStream(self, streams):
        threading.Thread(target=pub.subscribe, args=(self.handleLSLConnect, "streamConnect")).start()
        self.streamManager.connectStreams(streams)

    def resetStream(self):
        self.streamManager.resetStream()

    def handleLSLConnect(self, msg, settingsChannels, streamChannels):
        if msg == "CHANNELS_OKAY":
            self.setProgramPaused()

    # Starts the calibrationManager, in a thread, for saving the data of the calibration
    def startCalibration(self):
        self.programPaused = False
        self.calibrationManager = Calibration.CalibrationManager(self)
        self.setCalibrationOn(True)
        self.calibrationThread = threading.Thread(target=self.calibrationManager.startCalibration,
                                                  args=(self.streamManager.streamInlet,))
        self.calibrationThread.start()

    def stopCalibration(self):
        self.setCalibrationOn(False)
        self.calibrationThread.join()
        self.setProgramPaused()
        print("mods: ", self.modsTimestamp)

    def resetCalibration(self):
        self.stopCalibration()
        self.modsTimestamp = []
        self.modOnTimestamp = -1

    # Waits for the calibration-thread to join and calls the method handling
    # the SVM training
    def endCalibration(self):
        self.stopCalibration()
        if not self.modsTimestamp:
            self.resetCalibration()
            return False
        self.calibrationManager.startTraining()
        return True

    # gets the scores of the cross-validation of the SVM (after calibration)
    def getCrossValScores(self):
        return self.calibrationManager.crossValScores

    # saves the timestamp of the start of the modulation
    # if in livesystem, the sound-effect is started
    def startModulation(self):
        self.modOnTimestamp = pylsl.local_clock()
        if self.inLiveSystem:
            self.startMidiEffect()

    # saves the timestamp of the end of the modulation, together with the start:
    # (timestamp start, timestamp end) to the array holding all the modulation windows
    # if in livesystem, the sound-effect is ended
    def endModulation(self):
        self.modsTimestamp.append((self.modOnTimestamp, pylsl.local_clock()))
        if self.inLiveSystem:
            self.endMidiEffect()

    # calls the method which pulls samples from the LSL-stream, without saving them
    def keepPullingSamplesFromInlet(self):
        while self.programPaused:
            self.streamManager.keepPullingSamplesFromInlet()

    # starts the manager for the livesystem in a new thread
    def startLiveSystem(self):
        self.setInLiveSystem(True)
        self.modsTimestamp = []
        self.modOnTimestamp = -1

        if not self.calibrationManager.svm:
            print("ERROR: Program-Manager: YOU CANNOT START the system WITHOUT calibration!")
            return

        if not self.firstLiveRoundDone:
            self.midiManager.createMIDIOutport()
        self.liveSystemManager = Live.LiveSystemManager(self, self.calibrationManager.svm)

        self.programPaused = False
        self.programPauseThread.join()

        self.liveSystemThread = threading.Thread(target=self.liveSystemManager.startSystem,
                                                 args=(self.streamManager.streamInlet,))
        self.liveSystemThread.start()

    # stops the livesystem and waits for the thread to join
    def stopLiveSystem(self):
        self.setInLiveSystem(False)
        self.firstLiveRoundDone = True
        self.liveSystemThread.join()
        self.programPaused = True
        threading.Thread(target=self.keepPullingSamplesFromInlet).start()

    def quit(self):
        self.programPaused = False
        sys.exit()


def main():
    programMaster = ProgramMaster()
    print("thread in main: ", threading.current_thread())
    programMaster.startWindow()
