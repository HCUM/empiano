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
import helpers.SettingsManager as SettingsManager
import livesystem.CalibrationManager as Calibration
import livesystem.gui.GuiController as GuiController

###########################################################################
# Class ProgramMaster
# -> everything goes through here, manages all the sub-classes
###########################################################################
class ProgramMaster:
    def __init__(self):
        self.streamManager = StreamManager.StreamManager(self)

        self.programPauseThread = None
        self.programPaused = False

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

        self.tmsmtpSem = threading.Semaphore()
        self.tmstmpLastPrediction = None
        self.tmstmpLastTwoSamples = deque([None, None])

        self.modOnTimestamp = -1
        self.modsTimestamp = []  # saves all the timestamp pairs of the modulations: [(begin, end), ...]

    # Run gui for the live-system
    def startWindow(self):
        self.guiController.launchWindow()

    # Getters with semaphore

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

    def getLatencyInfo(self):
        self.tmsmtpSem.acquire()
        res = copy.deepcopy(self.tmstmpLastTwoSamples)
        self.tmsmtpSem.release()
        return res

    # Setters with semaphore

    def setCalibrationOn(self, boolean):
        self.calibrationSem.acquire()
        self.calibrationOn = boolean
        self.calibrationSem.release()

    def setInLiveSystem(self, boolean):
        self.liveSystemSem.acquire()
        self.inLiveSystem = boolean
        self.liveSystemSem.release()

    # param: augmentationOn = current prediction of the SVM whether an augmentation was performed or not;
    # Starts or ends the sound effect, when needed; updates the lastTwoPredictions field
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

    def setLastSampleTimestamp(self, tmstmp):
        self.tmsmtpSem.acquire()
        self.tmstmpLastTwoSamples.popleft()
        self.tmstmpLastTwoSamples.append(tmstmp)
        self.tmsmtpSem.release()

    # Starts the midiManager for sending the midi sound effect, in a thread
    def startMidiEffect(self):
        self.midiEffectOn = True
        self.midiEffectThread = threading.Thread(target=self.midiManager.sendEffect)
        self.midiEffectThread.start()

    # Sets the midi sound effect on false and waits for the thread handling the effect to join
    def endMidiEffect(self):
        self.midiEffectOn = False
        self.midiEffectThread.join()

    # Checks whether the (in the settings) specified MIDI-cable can be found
    def checkIfMidiCableCanBeFound(self, midiCableName):
        return self.midiManager.findMidiCable(midiCableName)

    # Initializes the connection to the defined LSL-stream
    def connectToLSLStream(self, streams):
        threading.Thread(target=pub.subscribe, args=(self.handleLSLConnect, "streamConnect")).start()
        self.streamManager.connectStreams(streams)

    # If the connection to the LSL-stream was successful, the program is paused so it pulls the incoming samples
    # Pub-message sent in StreamManager.connectStreams
    def handleLSLConnect(self, msg, settingsChannels, streamChannels):
        if msg == "CHANNELS_OKAY":
            self.setProgramPaused()

    # Calls the method to reset the LSL-stream
    def resetStream(self):
        if self.programPaused:
            self.programPaused = False
        self.streamManager.resetStream()

    # Starts the calibrationManager, in a thread, for saving the data of the calibration
    def startCalibration(self):
        self.programPaused = False
        self.calibrationManager = Calibration.CalibrationManager(self)
        self.setCalibrationOn(True)
        self.calibrationThread = threading.Thread(target=self.calibrationManager.startCalibration,
                                                  args=(self.streamManager.streamInlet,))
        self.calibrationThread.start()

    # Stops the calibration and pauses the program, so it keeps pulling the samples from the LSL-stream
    def stopCalibration(self):
        self.setCalibrationOn(False)
        self.calibrationThread.join()
        if not self.programPaused:
            self.setProgramPaused()

    # Resets the calibration and all the variables
    def resetCalibration(self):
        self.stopCalibration()
        self.modsTimestamp = []
        self.modOnTimestamp = -1
        self.firstLiveRoundDone = False
        self.midiManager.output = None
        self.setInLiveSystem(False)

    # Waits for the calibration-thread to join and calls the method handling
    # the SVM training
    def endCalibration(self, lengthMods=None):
        self.stopCalibration()
        if not self.modsTimestamp or (lengthMods and lengthMods != len(self.modsTimestamp)):
            self.resetCalibration()
            return "Tracking of the modulations failed."
        result = self.calibrationManager.startTraining()
        if result:
            return result
        return None

    # Gets the scores of the cross-validation of the SVM (after calibration)
    def getCrossValScores(self):
        return self.calibrationManager.crossValScores

    # Saves the timestamp of the start of the modulation
    # If in livesystem, the sound-effect is started
    def startModulation(self):
        self.modOnTimestamp = pylsl.local_clock()
        if self.inLiveSystem:
            self.startMidiEffect()

    # Saves the timestamp of the end of the modulation, together with the start:
    # (timestamp start, timestamp end) to the array holding all the modulation windows
    # If in livesystem, sound-effect is ended
    def endModulation(self):
        self.modsTimestamp.append((self.modOnTimestamp, pylsl.local_clock()))
        if self.inLiveSystem:
            self.endMidiEffect()

    # Calls the method which pulls samples from the LSL-stream, without saving them
    def keepPullingSamplesFromInlet(self):
        while self.programPaused:
            self.streamManager.keepPullingSamplesFromInlet()

    # Starts the manager for the livesystem in a new thread and if necessary creates the MIDI outport
    def startLiveSystem(self):
        self.setInLiveSystem(True)
        self.modsTimestamp = []
        self.modOnTimestamp = -1

        if not self.firstLiveRoundDone:
            self.midiManager.createMIDIOutport()
        self.liveSystemManager = Live.LiveSystemManager(self, self.calibrationManager.svm)

        self.programPaused = False
        self.programPauseThread.join()

        self.liveSystemThread = threading.Thread(target=self.liveSystemManager.startSystem,
                                                 args=(self.streamManager.streamInlet,))
        self.liveSystemThread.start()

    # Stops the livesystem and waits for the thread to join
    def stopLiveSystem(self):
        self.setInLiveSystem(False)
        self.firstLiveRoundDone = True
        self.liveSystemThread.join()
        self.setProgramPaused()
        self.midiManager.sendPitchWheelStopMsg()

    def quit(self):
        self.programPaused = False
        sys.exit()


def main():
    programMaster = ProgramMaster()
    SettingsManager.readConfigFile()
    programMaster.startWindow()
