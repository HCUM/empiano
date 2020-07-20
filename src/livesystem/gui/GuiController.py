import livesystem.gui.Window as window

class guiController:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.calibrationDone = False
        self.lslConnected = False
        self.app = window.App(self)
        self.liveSystemRound = 0

    def getCalibration(self):
        return self.calibrationDone

    def getLslConnection(self):
        return self.lslConnected

    def launchWindow(self):
        self.app.showWindow()

    # methods which change the frames shown in the window
    def showConnectFrame(self):
        self.app.showFrame(window.LSLPage)

    def showOfflineCaliWindow(self):
        self.app.showFrame(window.OfflineCaliPage)
        self.programMaster.startOfflineCalibration()

    def showCalibrationWindow(self):
        self.app.showFrame(window.CaliPage)

    def showTestSysWindow(self):
        self.app.showFrame(window.SysPage)
        self.programMaster.startTestSystem()

    def showNowSysWindow(self):
        self.app.showFrame(window.NowSysPage)


    # methods triggered by buttons etc

    # calls the method for connecting to the LSL-stream, given the type and value of the connection
    def connectToLSLStream(self, connectionType, connectionVal):
        self.app.showFrame(window.CaliPage)
        self.programMaster.connectToLSLStream(connectionType, connectionVal)

    # calls the method for starting the livesystem
    def startLiveSystem(self):
        self.liveSystemRound += 1
        self.app.showFrame(window.SysPage)
        self.programMaster.startLiveSystem()

    def showSettingsWindow(self):
        self.app.showFrame(window.SettingPage)

    def startFakeCali(self):
        self.programMaster.startFakeCali()

    # calls the method starting the calibration
    def startCali(self):
        self.programMaster.startCalibration()
        #self.app.showFrame(window.CaliAnimationPage)

    # calls the method ending the calibration
    def endCali(self):
        self.programMaster.endCalibration()
        self.app.showFrame(window.NowSysPage)

    # calls the method starting the modulation
    def startMod(self):
        #self.liveSysManager.modulation(on=True)
        self.programMaster.startMod()

    # calls the method ending the modulation
    def endMod(self):
        #self.liveSysManager.modulation(on=False)
        self.programMaster.endMod()

    # calls the method stopping the livesystem
    def stopSystem(self):
        self.programMaster.stopSystem(self.liveSystemRound)
        self.app.showFrame(window.NowSysPage)

    # quitting the system and the window
    def quit(self):
        self.app.window.destroy()
        self.programMaster.quit()

    def startWizardOfOzSound(self):
        self.programMaster.setWizardOfOzSound()
