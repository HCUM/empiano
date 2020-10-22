import livesystem.gui.wxWindow as wxwindow
import wx


class guiController:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.app = None
        self.mainFrame = None

    def launchWindow(self):
        self.app = wx.App(False)
        self.mainFrame = wxwindow.MyFrame(self)
        self.mainFrame.Show()
        self.app.MainLoop()

    # Methods triggered by buttons etc

    # Calls the method which checks whether the (in the settings) specified MIDI cable can be found
    def checkIfMidiCableCanBeFound(self, midiCableName):
        return self.programMaster.checkIfMidiCableCanBeFound(midiCableName)

    # Updates the values changed in the settings
    def updateSettings(self, amtElectrodes, midiCableName, shouldCreateMidiCable):
        self.programMaster.updateSettings(amtElectrodes, midiCableName, shouldCreateMidiCable)

    # Calls the method for connecting to the LSL-stream, given the list of streams chosen in the UI
    def connectToLSLStream(self, streams):
        self.programMaster.connectToLSLStream(streams)

    # Calls the method resetting the LSL-stream
    def resetStream(self):
        self.programMaster.resetStream()

    # Calls the method starting the calibration
    def startCalibration(self):
        self.programMaster.startCalibration()

    # Calls the method ending the calibration
    def endCalibration(self, lengthMods=None):
        return self.programMaster.endCalibration(lengthMods)

    # Calls the method stopping the calibration
    def stopCalibration(self):
        self.programMaster.stopCalibration()

    # Calls the method resetting the calibration
    def resetCalibration(self):
        self.programMaster.resetCalibration()

    # Gets the current prediction
    def getPredictionFromMaster(self):
        return self.programMaster.getCurrentPrediction()

    # Gets the value of the liveSystemOn field
    def getLiveSysFromMaster(self):
        return self.programMaster.getLiveSystemOn()

    # Gets the scores of the cross-validation of the SVM (after calibration)
    def getCrossValScores(self):
        return self.programMaster.getCrossValScores()

    # Calls the method starting the modulation
    def startModulation(self):
        self.programMaster.startModulation()

    # Calls the method ending the modulation
    def endModulation(self):
        self.programMaster.endModulation()

    # Calls the method for starting the livesystem
    def startLiveSystem(self):
        self.programMaster.startLiveSystem()

    # Calls the method stopping the livesystem
    def stopLiveSystem(self):
        self.programMaster.stopLiveSystem()

    # Calls the method pausing the program
    def setProgramPaused(self):
        self.programMaster.setProgramPaused()

    # Quitting the system and destroying the window
    def quit(self):
        self.app.Destroy()
        self.programMaster.quit()

    # Used for changing the panel displayed in the window, if wished the window is refreshed afterwards
    def showPanel(self, currentPanel, nextPanel, refresh=False):
        currentPanel.Hide()
        panel = currentPanel.Parent.panels[nextPanel]
        panel.Show()
        if refresh:
            self.mainFrame.Refresh()
            panel.Update()
