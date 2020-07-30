from tkinter import *

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
        for page in (StartPage, CalibrationPage, LSLPage, InLiveSystemPage, StartLiveSystemPage):
            frame = page(self.container, self.controller, self.width, self.height)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.window.bind("<KeyPress>", self.keydown)
        self.modon = False

    # using the space key, the beginning and end of the modulation can be tracked
    # -> used during the calibration
    def keydown(self, event):
        if event.keysym == 'space':
            if self.modon:
                self.controller.endModulation()
                self.modon = False
            else:
                self.controller.startModulation()
                self.modon = True


    def showWindow(self):
        self.showFrame(StartPage)
        self.window.mainloop()

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# entrance page to the system
class StartPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.empianoText = Label(self, text="EMPiano", fg='#009440', font="Helvetica 70 bold")
        self.startButton = Button(self, text="Start", command=controller.showConnectFrame)

        self.empianoText.grid(row = 0, padx=10, pady=50)
        self.startButton.grid(row=1)


# page shown, when calibration is on
class CalibrationPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)
        self.controller = controller
        text = Label(self, text="CALIBRATION TIME, COME ON!")
        text.grid(row=1, column=1)
        self.startStopBut = Button(self, text="Start", command=self.handleCali)
        self.startStopBut.grid(row=2, column=1)

    # starts and ends the calibration
    def handleCali(self):
        if self.startStopBut.cget('text') == "Start":
            self.controller.startCalibration()
            self.startStopBut.configure(text="Stop")
        else:
            self.controller.endCalibration()


# page for going into the livesystem; here: program on pause
class StartLiveSystemPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)

        text   = Label(self, text="START LIVE_SYSTEM NOW!")
        button = Button(self, text="Go to Live System", command=controller.startLiveSystem)
        quitBut = Button(self, text="Quit", command=controller.quit)

        text.grid(row=1, column=1)
        button.grid(row=2, column=1)
        quitBut.grid(row=3, column=1)


# page during the livesystem
class InLiveSystemPage(Frame):
    def __init__(self, parent, controller, width, height):
        Frame.__init__(self, parent)

        self.controller = controller
        self.text   = Label(self, text="LIVE_SYSTEM, START NEW ROUND!",)
        self.button = Button(self, text="Stop", command=self.controller.stopLiveSystem)

        self.text.grid(row=1, column=1)
        self.button.grid(row=2, column=1)


# page for connecting to the LSL-stream
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

        connectButton = Button(self, text="Connect",
                               command=lambda: controller.connectToLSLStream(tkvar.get(), entry.get()))
        connectButton.grid(row=2, columnspan=2, pady=pady)