import livesystem.gui.wxWindow as wxwindow
import wx

class guiController:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.app: wx.App

    def launchWindow(self):
        self.app = wx.App(False)
        frame = wxwindow.MyFrame(self)
        frame.Show()
        self.app.MainLoop()


    # methods triggered by buttons etc

    # updates the values changed in the settings
    def updateSettings(self, amtElectrodes, midiCableName, shouldCreateMidiCable):
        self.programMaster.updateSettings(amtElectrodes, midiCableName, shouldCreateMidiCable)

    # calls the method for connecting to the LSL-stream, given the type and value of the connection
    def connectToLSLStream(self):#, connectionType, connectionVal):
        self.programMaster.connectToLSLStream()#connectionType, connectionVal)

    def checkStreamAvailability(self):
        self.programMaster.checkStreamAvailability()

    # calls the method starting the calibration
    def startCalibration(self):
        self.programMaster.startCalibration()

    # calls the method ending the calibration
    def endCalibration(self):
        self.programMaster.endCalibration()

    # calls the method starting the modulation
    def startModulation(self):
        self.programMaster.startModulation()

    # calls the method ending the modulation
    def endModulation(self):
        self.programMaster.endModulation()

    # calls the method for starting the livesystem
    def startLiveSystem(self):
        self.programMaster.startButtonPressed()

    # calls the method stopping the livesystem
    def stopLiveSystem(self):
        self.programMaster.stopLiveSystem()

    # quitting the system and the window
    def quit(self):
        self.app.Destroy()
        self.programMaster.quit()
