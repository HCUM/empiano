import livesystem.gui.Window as window

class guiController:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.app = window.App(self)
        self.liveSystemRound = 0

    def launchWindow(self):
        self.app.showWindow()

    # methods which change the frames shown in the window
    def showConnectFrame(self):
        self.app.showFrame(window.LSLPage)


    def showCalibrationWindow(self):
        self.app.showFrame(window.CalibrationPage)

    def showTestSysWindow(self):
        self.app.showFrame(window.InLiveSystemPage)
        self.programMaster.startTestSystem()

    def showNowSysWindow(self):
        self.app.showFrame(window.StartLiveSystemPage)


    # methods triggered by buttons etc

    def connectToLSLStream(self, connectionType, connectionVal):
        self.app.showFrame(window.CalibrationPage)
        self.programMaster.connectToLSLStream(connectionType, connectionVal)

    def showSettingsWindow(self):
        self.app.showFrame(window.SettingPage)

    def startCali(self):
        self.programMaster.startCalibration()

    def endCali(self):
        self.programMaster.endCalibration()
        self.app.showFrame(window.StartLiveSystemPage)

    def startMod(self):
        self.programMaster.startMod()

    def endMod(self):
        self.programMaster.endMod()

    def startLiveSystem(self):
        self.liveSystemRound += 1
        self.app.showFrame(window.InLiveSystemPage)
        self.programMaster.startLiveSystem()

    def stopLiveSystem(self):
        self.programMaster.stopLiveSystem()
        self.app.showFrame(window.StartLiveSystemPage)

    def quit(self):
        self.app.window.destroy()
        self.programMaster.quit()
