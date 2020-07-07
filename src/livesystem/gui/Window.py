from tkinter import *
from storage import Constants

class App:
    def __init__(self, controller):
        self.controller = controller

        self.window = Tk()
        self.window.title("EMPiano")
        self.height = 220
        self.width  = 322
        self.window.geometry(str(self.width)+"x"+str(self.height))

        self.container = Frame(self.window)
        self.container.grid(row=0, column=0, sticky="nsew")
        #frames
        self.frames= {}
        for page in (StartPage, CaliPage, LSLPage, SysPage, OfflineCaliPage, NowSysPage, CaliAnimationPage):
            frame = page(self.container, self.controller, self.width, self.height)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        #buttons
        self.caliButton: Button
        self.testSystemButton: Button
        self.settingsButton: Button
        self.connectButton: Button

        self.window.bind("<KeyPress>", self.keydown)
        self.modon = False


    def keydown(self, event):
        #space pressed -> to track the beginning and end of modulation
        if event.keysym == 'space':
            if self.modon:
                self.controller.endMod()
                self.modon = False
            else:
                self.controller.startMod()
                self.modon = True
        #
        elif event.keysym == 'w':
            print("turned on wizard of oz")
            self.controller.startWizardOfOzSound()


    def showWindow(self):
        self.showFrame(StartPage)
        self.window.mainloop()

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont is CaliAnimationPage:
            frame.pause()


class StartPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.empianoText = Label(self, text="EMPiano", fg='#009440', font="Helvetica 70 bold")
        self.startButton = Button(self, text="Start", command=controller.showConnectFrame)
        #self.offlineCaliBut = Button(self, text="Offline Calibration", command=controller.showOfflineCaliWindow)
        #self.fakeLiveCaliBut = Button(self, text="fake live calibration", command=controller.startFakeCali)

        self.empianoText.grid(row = 0, padx=10, pady=50)#, column= 0, columnspan=3)
        self.startButton.grid(row=1)#, column=0)
        #self.fakeLiveCaliBut.grid(row=1, column=1)
        #self.offlineCaliBut.grid(row=1, column=2)



class CaliPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.controller = controller
        text = Label(self, text="CALIBRATION TIME, COME ON!")
        text.grid(row=1, column=1)
        self.startStopBut = Button(self, text="Start", command=self.handleCali)
        self.startStopBut.grid(row=2, column=1)

    def handleCali(self):
        if self.startStopBut.cget('text') == "Start":
            self.controller.startCali()
            self.startStopBut.configure(text="Stop")
        else:
            self.controller.endCali()

    def handleModulation(self):
        if self.modBut.cget('text') == "Start Modulation":
            self.modBut.configure(text="Stop Modulation")
            self.controller.startMod()
        else:
            self.modBut.configure(text="Start Modulation")
            self.controller.endMod()


class CaliAnimationPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.controller = controller

        self.currentTaskLabel = Label(self, text="")
        self.timerLabel = Label(self, text="")
        self.nextTaskLabel = Label(self, text="next: ")

        self.currentTaskLabel.grid(row=1, column=1)
        self.timerLabel.grid(row=2, column=1)
        self.nextTaskLabel.grid(row=3, column=1)

        self.currentCalibrationTaskIndex = 0

        self.pauseTime = Constants.secondsOfCaliPause
        self.taskTime  = Constants.secondsOfCaliTasks


    def handleCalibration(self):
        currentTask = Constants.calibrationOrder[self.currentCalibrationTaskIndex]

        self.currentTaskLabel.configure(text=currentTask)
        self.timerLabel.configure(text=str(self.taskTime))

        if self.taskTime == Constants.secondsOfCaliTasks:
            if 'mod' in currentTask:
                self.controller.startMod()

        elif self.taskTime == 0:
            if 'mod' in currentTask:
                self.controller.endMod()
            if self.currentCalibrationTaskIndex +1 == len(Constants.calibrationOrder):
                self.controller.endCali()
                return
            self.currentCalibrationTaskIndex += 1
            self.taskTime = Constants.secondsOfCaliTasks
            self.currentTaskLabel.configure(text="")
            self.pause()
            return

        self.taskTime -= 1
        self.after(1000, self.handleCalibration)

    def pause(self):
        self.timerLabel.configure(text=str(self.pauseTime))
        self.nextTaskLabel.configure(text="next: "+Constants.calibrationOrder[self.currentCalibrationTaskIndex])
        if self.pauseTime == 0:
            self.pauseTime = Constants.secondsOfCaliPause
            self.nextTaskLabel.configure(text="")
            self.handleCalibration()
            return
        self.pauseTime -= 1
        self.after(1000, self.pause)



class NowSysPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)

        text   = Label(self, text="START LIVE_SYSTEM NOW!")
        button = Button(self, text="Go to Live System", command=controller.startLiveSystem)
        quitBut = Button(self, text="Quit", command=controller.quit)

        text.grid(row=1, column=1)
        button.grid(row=2, column=1)
        quitBut.grid(row=3, column=1)



class SysPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)

        self.controller = controller
        self.text   = Label(self, text="LIVE_SYSTEM, START NEW ROUND!",)
        self.button = Button(self, text="Stop", command=self.controller.stopSystem)

        self.text.grid(row=1, column=1)
        self.button.grid(row=2, column=1)



class LSLPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        text = Label(self, text="Connect to LSL stream")
        pady = (height - (3*25))/6  #3 rows, with height ~25 and each row has 2*pady -> 6
        padx = 5 #just random to test
        text.grid(row=0, column=0, columnspan=2, pady=pady)

        #OptionMenu
        # Create a Tkinter variable
        tkvar = StringVar(self)
        # Dictionary with options
        choices = {'type', 'name'}
        tkvar.set('type')  # set the default option

        optionMenu = OptionMenu(self, tkvar, *choices)
        optionMenu.grid(row=1, column=0, pady=pady, padx=padx)

        #text field
        entryVar = StringVar(self)
        entryVar.set("EEG")
        entry = Entry(self, textvariable=entryVar)
        entry.grid(row=1, column=1, pady=pady, padx=padx)

        connectButton = Button(self, text="Connect", command=lambda: controller.connectToLSLStream(tkvar.get(), entry.get()))
        connectButton.grid(row=2, columnspan=2, pady=pady)

class OfflineCaliPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        button = Button(self, text="Go to Live System", command=controller.showTestSysWindow)
        button.grid(row=1, column=1)