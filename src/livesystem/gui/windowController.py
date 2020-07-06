import livesystem.gui.window as window

class windowController:

    def __init__(self, liveSysManager):
        self.liveSysManager = liveSysManager
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

    def showConnectFrame(self):
        self.app.showFrame(window.LSLPage)

    def connectToLSLStream(self, connectionType, connectionVal):
        self.app.showFrame(window.CaliPage)
        self.liveSysManager.connectToLSLStream(connectionType, connectionVal)

    def showOfflineCaliWindow(self):
        self.app.showFrame(window.OfflineCaliPage)
        self.liveSysManager.startOfflineCalibration()

    def showCalibrationWindow(self):
        self.app.showFrame(window.CaliPage)

    def showTestSysWindow(self):
        self.app.showFrame(window.SysPage)
        self.liveSysManager.startTestSystem()

    def showNowSysWindow(self):
        self.app.showFrame(window.NowSysPage)


    def startLiveSystem(self):
        self.liveSystemRound += 1
        self.app.showFrame(window.SysPage)
        self.liveSysManager.startLiveSystem()

    def showSettingsWindow(self):
        self.app.showFrame(window.SettingPage)

    def startFakeCali(self):
        self.liveSysManager.startFakeCali()

    def startCali(self):
        self.liveSysManager.startCalibration()
        #self.app.showFrame(window.CaliAnimation)

    def endCali(self):
        self.liveSysManager.endCalibration()
        self.app.showFrame(window.NowSysPage)

    def startMod(self):
        #self.liveSysManager.modulation(on=True)
        self.liveSysManager.startMod()

    def endMod(self):
        #self.liveSysManager.modulation(on=False)
        self.liveSysManager.endMod()

    def stopSystem(self):
        self.liveSysManager.stopSystem(self.liveSystemRound)
        self.app.showFrame(window.NowSysPage)

    def quit(self):
        self.app.window.destroy()
        self.liveSysManager.quit()

    def startWizardOfOzSound(self):
        self.liveSysManager.setWizardOfOzSound()
