import livesystem.gui.Window as window
import livesystem.gui.wxWindow as wxwindow
import wx


class guiController:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        #self.app = window.App(self)
        self.liveSystemRound = 0

    def launchWindow(self):
        #self.app.showWindow()
        app = wx.App(False)
        frame = wxwindow.MyFrame(self)
        frame.Show()
        app.MainLoop()

    # methods which change the frames shown in the window
    def showConnectFrame(self):
        self.app.showFrame(window.LSLPage)

    # methods triggered by buttons etc

    # updates the values changed in the settings
    def updateSettings(self, amtElectrodes, midiCableName, shouldCreateMidiCable):
        self.programMaster.updateSettings(amtElectrodes, midiCableName, shouldCreateMidiCable)

    # calls the method for connecting to the LSL-stream, given the type and value of the connection
    def connectToLSLStream(self, connectionType, connectionVal):
        #self.app.showFrame(window.CalibrationPage)
        self.programMaster.connectToLSLStream(connectionType, connectionVal)

    # calls the method starting the calibration
    def startCalibration(self):
        self.programMaster.startCalibration()

    # calls the method ending the calibration
    def endCalibration(self):
        self.programMaster.endCalibration()
        #self.app.showFrame(window.StartLiveSystemPage)

    # calls the method starting the modulation
    def startModulation(self):
        self.programMaster.startModulation()

    # calls the method ending the modulation
    def endModulation(self):
        self.programMaster.endModulation()

    # calls the method for starting the livesystem
    def startLiveSystem(self):
        self.liveSystemRound += 1
        #self.app.showFrame(window.InLiveSystemPage)
        self.programMaster.startButtonPressed()

    # calls the method stopping the livesystem
    def stopLiveSystem(self):
        self.programMaster.stopLiveSystem()
        #self.app.showFrame(window.StartLiveSystemPage)

    # quitting the system and the window
    def quit(self):
        #self.app.window.destroy()
        self.programMaster.quit()
