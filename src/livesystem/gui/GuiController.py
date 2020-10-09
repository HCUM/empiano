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


    # methods triggered by buttons etc

    # calls the method which checks whether the (in the settings) specified MIDI cable can be found
    def checkIfMidiCableCanBeFound(self, midiCableName):
        return self.programMaster.checkIfMidiCableCanBeFound(midiCableName)

    # updates the values changed in the settings
    def updateSettings(self, amtElectrodes, midiCableName, shouldCreateMidiCable):
        self.programMaster.updateSettings(amtElectrodes, midiCableName, shouldCreateMidiCable)

    # calls the method for connecting to the LSL-stream, given the list of streams chosen in the UI
    def connectToLSLStream(self, streams):
        self.programMaster.connectToLSLStream(streams)

    def resetStream(self):
        self.programMaster.resetStream()

    # calls the method starting the calibration
    def startCalibration(self):
        self.programMaster.startCalibration()

    # calls the method ending the calibration
    def endCalibration(self):
        self.programMaster.endCalibration()

    def stopCalibration(self):
        self.programMaster.stopCalibration()

    def resetCalibration(self):
        self.programMaster.resetCalibration()

    def updateView(self, prediction):
        #self.
        pass

    def getPredictionFromMaster(self):
        return self.programMaster.getCurrentPrediction()

    def getLiveSysFromMaster(self):
        return self.programMaster.getLiveSystemOn()

    # gets the scores of the cross-validation of the SVM (after calibration)
    def getCrossValScores(self):
        return self.programMaster.getCrossValScores()

    # calls the method starting the modulation
    def startModulation(self):
        self.programMaster.startModulation()

    # calls the method ending the modulation
    def endModulation(self):
        self.programMaster.endModulation()

    # calls the method for starting the livesystem
    def startLiveSystem(self):
        self.programMaster.startLiveSystem()

    # calls the method stopping the livesystem
    def stopLiveSystem(self):
        self.programMaster.stopLiveSystem()

    # calls the method pausing the program
    def setProgramPaused(self):
        self.programMaster.setProgramPaused()

    # quitting the system and destroying the window
    def quit(self):
        self.app.Destroy()
        self.programMaster.quit()

    # used for changing the panel displayed in the window
    def showPanel(self, currentPanel, nextPanel, refresh=False):
        currentPanel.Hide()
        panel = currentPanel.Parent.panels[nextPanel]
        panel.Show()
        if refresh:
            print("about to refresh the frame")
            self.mainFrame.Refresh()
            panel.Update()
            #self.mainFrame.Update()

