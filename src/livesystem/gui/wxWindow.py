# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder (version 3.9.0 Jul 27 2020)
# http://www.wxformbuilder.org/
###########################################################################

import wx
import os
import time
import wx.xrc
import wx.grid
import platform
import threading
from pubsub import pub
from wx.lib.intctrl import IntCtrl
from wx.media import MediaCtrl, EVT_MEDIA_STOP
import storage.Constants as Constants

frameSize = wx.Size(1000, 600)
backgroundColorWindows = wx.Colour(0xE6, 0xE6, 0xE6)
Continue = 0
Go_to_settings = 1
Back_to_streams = 2


class MyFrame(wx.Frame):
    def __init__(self, controller):
        wx.Frame.__init__(self, None, wx.ID_ANY, title=u"EMPiano", size=frameSize)
        self.controller = controller
        self.platform = platform.platform()
        self.isWindows = self.platform.startswith("Windows")
        if self.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)
        self.backToConnectPage = False

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.AddStretchSpacer(prop=1)

        self.panels = {}
        for panel in (StartPanel, SettingsPanel, LiveSystemPanel,
                      CustomCalibrationPanel, StreamOverviewPanel,
                      ChooseCalibrationPanel, InbuiltCalibrationPanel):
            newPanel = panel(self, self.controller)
            self.panels[panel] = newPanel
            newPanel.Hide()
            self.sizer.Add(newPanel, 1, wx.EXPAND)

        panel = self.panels[StartPanel]
        panel.Show()

        self.Bind(wx.EVT_CLOSE, self.quit)

        self.sizer.AddStretchSpacer(prop=1)
        self.SetSizer(self.sizer)

    def quit(self, event):
        event.Skip()
        self.controller.quit()


###########################################################################
# Class StartPanel
###########################################################################

class StartPanel(wx.Panel):

    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)

        verticalBoxes = wx.BoxSizer(wx.VERTICAL)

        self.empianoLabel = wx.StaticText(self, wx.ID_ANY, u"EMPiano", wx.DefaultPosition,
                                          wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL)
        self.empianoLabel.Wrap(-1)
        self.empianoLabel.SetFont(wx.Font(60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                          wx.FONTWEIGHT_BOLD, False, "Arial Black"))
        self.empianoLabel.SetForegroundColour(wx.Colour(17, 133, 49))

        verticalBoxes.Add(self.empianoLabel, 0, wx.ALL | wx.EXPAND, 5)
        verticalBoxes.Add((0, 70), 0, wx.EXPAND, 5)

        self.startButton = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.startButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        verticalBoxes.Add((0, 20), 0, wx.EXPAND, 5)

        self.settingsButton = wx.Button(self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0)

        verticalBoxes.Add(self.settingsButton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.startButton.Bind(wx.EVT_BUTTON, self.showLSLPanel)
        self.settingsButton.Bind(wx.EVT_BUTTON, self.showSettingsPanel)

        self.SetSizer(verticalBoxes)
        self.Layout()

    def showLSLPanel(self, event):
        event.Skip()
        self.controller.showPanel(self, StreamOverviewPanel)

    def showSettingsPanel(self, event):
        event.Skip()
        self.controller.showPanel(self, SettingsPanel)

    def quitButtonPressed(self, event):
        event.Skip()
        self.controller.quit()


###########################################################################
# Class SettingsPanel
###########################################################################

class SettingsPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        self.parent = parent
        self.controller = controller
        if self.parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)

        verticalBoxes = wx.BoxSizer(wx.VERTICAL)

        verticalBoxes.Add((0, 0), 1, wx.EXPAND, 5)

        self.dataAcquisitionLabel = wx.StaticText(self, wx.ID_ANY, u"EMG - Data Acquisition", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.dataAcquisitionLabel.Wrap(-1)
        self.dataAcquisitionLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande"))
        self.dataAcquisitionLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        verticalBoxes.Add(self.dataAcquisitionLabel, 0, wx.EXPAND | wx.ALL, 5)

        flexGridDataAcquisition = wx.FlexGridSizer(0, 2, 0, 57)
        flexGridDataAcquisition.AddGrowableCol(0)
        flexGridDataAcquisition.SetFlexibleDirection(wx.BOTH)
        flexGridDataAcquisition.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.amtChannelsLabel = wx.StaticText(self, wx.ID_ANY, u"Amount of Electrodes/Channels: ", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.amtChannelsLabel.Wrap(-1)
        flexGridDataAcquisition.Add(self.amtChannelsLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.amtElectrodesInput = IntCtrl(self, wx.ID_ANY, Constants.numberOfChannels, wx.DefaultPosition,
                                          wx.DefaultSize, wx.TE_RIGHT, min=1, allow_none=False)
        flexGridDataAcquisition.Add(self.amtElectrodesInput, 0, wx.ALL, 5)
        self.amtElectrodesInput.SetFocus()

        verticalBoxes.Add(flexGridDataAcquisition, 0, wx.ALL | wx.EXPAND, 5)

        self.preprocessingLabel = wx.StaticText(self, wx.ID_ANY, u"Preprocessing - Filters", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.preprocessingLabel.Wrap(-1)

        self.preprocessingLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande"))
        self.preprocessingLabel.SetForegroundColour(wx.Colour(17, 133, 49))

        verticalBoxes.Add(self.preprocessingLabel, 0, wx.ALL, 5)

        flexGridPreprocessing = wx.FlexGridSizer(0, 2, 0, 0)
        flexGridPreprocessing.AddGrowableCol(0)
        flexGridPreprocessing.SetFlexibleDirection(wx.BOTH)
        flexGridPreprocessing.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.lowCutoffBandpassLabel = wx.StaticText(self, wx.ID_ANY, u"Low Cutoff Frequency for Bandpass Filter:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.lowCutoffBandpassLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.lowCutoffBandpassLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.lowBandpassInput = wx.TextCtrl(self, wx.ID_ANY, str(Constants.lowerBoundCutOutFreq), wx.DefaultPosition,
                                            wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.lowBandpassInput, 0, wx.ALL | wx.LEFT, 5)

        self.highCutoffBandpassLabel = wx.StaticText(self, wx.ID_ANY,
                                                     u"High Cutoff Frequency for Bandpass Filter:\n",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.highCutoffBandpassLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.highCutoffBandpassLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.highBandpassInput = wx.TextCtrl(self, wx.ID_ANY, str(Constants.upperBoundCutOutFreq), wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.highBandpassInput, 0, wx.ALL, 5)

        self.lowCutoffBandstopLabel = wx.StaticText(self, wx.ID_ANY, u"Low Cutoff Frequency for Bandstop Filter:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.lowCutoffBandstopLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.lowCutoffBandstopLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.lowBandstopInput = wx.TextCtrl(self, wx.ID_ANY, str(Constants.lowBandStopFreq), wx.DefaultPosition,
                                            wx.DefaultSize,
                                            wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.lowBandstopInput, 0, wx.ALL, 5)

        self.highCutoffBandstopLabel = wx.StaticText(self, wx.ID_ANY, u"High Cutoff Frequency for Bandstop Filter:",
                                                     wx.DefaultPosition, wx.DefaultSize, 0)
        self.highCutoffBandstopLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.highCutoffBandstopLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.high_bandstop_input = wx.TextCtrl(self, wx.ID_ANY, str(Constants.highBandStopFreq), wx.DefaultPosition,
                                               wx.DefaultSize,
                                               wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.high_bandstop_input, 0, wx.ALL, 5)

        verticalBoxes.Add(flexGridPreprocessing, 0, wx.ALL | wx.EXPAND, 5)

        self.svmSettingsLabel = wx.StaticText(self, wx.ID_ANY, u"SVM - Settings", wx.DefaultPosition, wx.DefaultSize, 0)
        self.svmSettingsLabel.Wrap(-1)

        self.svmSettingsLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande"))
        self.svmSettingsLabel.SetForegroundColour(wx.Colour(17, 133, 49))

        verticalBoxes.Add(self.svmSettingsLabel, 0, wx.ALL, 5)

        flexGridSVMSettings = wx.FlexGridSizer(2, 2, 0, 0)
        flexGridSVMSettings.AddGrowableCol(0)
        flexGridSVMSettings.SetFlexibleDirection(wx.BOTH)
        flexGridSVMSettings.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        verticalBoxSizerSVMLeft = wx.BoxSizer(wx.VERTICAL)

        self.windowSizeLabel = wx.StaticText(self, wx.ID_ANY, u"Size for Sliding Window (in s):", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.windowSizeLabel.Wrap(-1)
        verticalBoxSizerSVMLeft.Add(self.windowSizeLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.dataValCorrectionLabel = wx.StaticText(self, wx.ID_ANY, u"Value for Correcting the Data:",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.dataValCorrectionLabel.Wrap(-1)
        verticalBoxSizerSVMLeft.Add(self.dataValCorrectionLabel, 0, wx.ALL | wx.EXPAND, 5)

        flexGridSVMSettings.Add(verticalBoxSizerSVMLeft, 1, wx.EXPAND, 5)

        verticalBoxSizerSVMRight = wx.BoxSizer(wx.VERTICAL)

        self.windowSizeInput = wx.TextCtrl(self, wx.ID_ANY, str(Constants.windowSize), wx.DefaultPosition,
                                           wx.DefaultSize,
                                           wx.TE_READONLY | wx.TE_RIGHT)
        verticalBoxSizerSVMRight.Add(self.windowSizeInput, 0, wx.ALL, 5)

        self.dataValCorrectionInput = wx.TextCtrl(self, wx.ID_ANY, str(Constants.dataSampleCorrection),
                                                  wx.DefaultPosition,
                                                  wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        verticalBoxSizerSVMRight.Add(self.dataValCorrectionInput, 0, wx.ALL, 5)
        flexGridSVMSettings.Add(verticalBoxSizerSVMRight, 1, wx.EXPAND, 5)

        verticalBoxes.Add(flexGridSVMSettings, 0, wx.ALL | wx.EXPAND, 5)

        # MIDI Settings
        self.midiSettingsLabel = wx.StaticText(self, wx.ID_ANY, u"MIDI - Settings", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        self.midiSettingsLabel.Wrap(-1)
        self.midiSettingsLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande"))
        self.midiSettingsLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        verticalBoxes.Add(self.midiSettingsLabel, 0, wx.ALL, 5)

        flexGridMidiSettings = wx.FlexGridSizer(0, 2, 0, 50)
        flexGridMidiSettings.AddGrowableCol(0)
        flexGridMidiSettings.SetFlexibleDirection(wx.BOTH)
        flexGridMidiSettings.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.midiCableName = wx.StaticText(self, wx.ID_ANY, u"Name of the virtual MIDI cable:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.midiCableName.Wrap(-1)
        flexGridMidiSettings.Add(self.midiCableName, 0, wx.ALL, 5)

        self.midiCableNameInput = wx.TextCtrl(self, wx.ID_ANY, Constants.virtualMIDICable, wx.DefaultPosition,
                                              wx.Size(136, -1),
                                              wx.TE_RIGHT)
        flexGridMidiSettings.Add(self.midiCableNameInput, 0, wx.ALL, 5)
        verticalBoxes.Add(flexGridMidiSettings, 0, wx.EXPAND | wx.ALL, 5)

        flexGridCreateCable = wx.FlexGridSizer(0, 2, 0, 0)
        flexGridCreateCable.AddGrowableCol(0)
        flexGridCreateCable.AddGrowableCol(1)
        flexGridCreateCable.SetFlexibleDirection(wx.BOTH)
        flexGridCreateCable.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.createMidiCableLabel = wx.StaticText(self, wx.ID_ANY, u"Create virtual MIDI cable (using mido library):",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.createMidiCableLabel.Wrap(-1)

        flexGridCreateCable.Add(self.createMidiCableLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.createMidiCableCheckbox = wx.CheckBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                   0)
        self.createMidiCableCheckbox.SetValue(Constants.createMIDICable)
        flexGridCreateCable.Add(self.createMidiCableCheckbox, 0, wx.ALL, 5)

        verticalBoxes.Add(flexGridCreateCable, 0, wx.EXPAND | wx.ALL, 5)

        self.setSettingsButton = wx.Button(self, wx.ID_ANY, u"Done", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.setSettingsButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizerAndFit(verticalBoxes)
        self.Centre()
        self.Layout()

        # Connect Events
        self.setSettingsButton.Bind(wx.EVT_BUTTON, self.updateSettings)

    def updateSettings(self, event):
        event.Skip()
        name = self.midiCableNameInput.GetValue()
        if name == "":
            dial = wx.MessageDialog(None, 'Please enter the name of the desired virtual midi-cable!',
                                    'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()

        else:
            if not self.createMidiCableCheckbox.GetValue():
                success, name = self.controller.checkIfMidiCableCanBeFound(name)
                if not success:
                    dial = wx.MessageDialog(None, 'The entered name of the virtual midi-cable does not exist!',
                                            'Error', wx.OK | wx.ICON_ERROR)
                    dial.ShowModal()
                    return
            self.controller.updateSettings(self.amtElectrodesInput.GetValue(),
                                           name,
                                           self.createMidiCableCheckbox.GetValue())
            print("settings updated")
            if not self.parent.backToConnectPage:
                print("in if not backToConnectPage")
                self.controller.showPanel(self, StartPanel)
            else:
                self.controller.showPanel(self, StreamOverviewPanel)
                self.parent.backToConnectPage = False


###########################################################################
# Class LiveSystemPanel
###########################################################################

class LiveSystemPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)
        threading.Thread(target=pub.subscribe, args=(self.infoListener, "liveSystemPanelListener")).start()

        self.verticalBoxes = wx.BoxSizer(wx.VERTICAL)

        self.verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.livesystemLabel = wx.StaticText(self, wx.ID_ANY, u"Live-System", wx.DefaultPosition, wx.DefaultSize,
                                             wx.ALIGN_CENTER_HORIZONTAL)
        self.livesystemLabel.Wrap(-1)
        self.livesystemLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.livesystemLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        self.verticalBoxes.Add(self.livesystemLabel, 0, wx.EXPAND | wx.ALL, 5)

        self.infoLabel = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.ALIGN_CENTER_HORIZONTAL)
        self.infoLabel.Wrap(-1)
        self.infoLabel.SetLabel("Cross-Validation (Calibration): ")
        self.verticalBoxes.Add(self.infoLabel, 0, wx.EXPAND | wx.ALL, 30)

        self.startLiveSystemButton = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        self.verticalBoxes.Add(self.startLiveSystemButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.backButton = wx.Button(self, wx.ID_ANY, u"Back", wx.DefaultPosition, wx.DefaultSize, 0)
        self.verticalBoxes.Add(self.backButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.startLiveSystemButton.Bind(wx.EVT_BUTTON, self.startButtonPressed)
        self.backButton.Bind(wx.EVT_BUTTON, self.backButtonPressed)

        self.SetSizerAndFit(self.verticalBoxes)
        self.Centre()
        self.Layout()

    def setInfoLable(self, string):
        self.infoLabel.SetLabel(string)
        self.SetSizerAndFit(self.verticalBoxes)
        self.Centre()
        self.Layout()

    def infoListener(self, msg, arg):
        print("in info listener")
        print("current active threads: ", threading.active_count())
        if msg == "CROSS_VAL_SET":
            stringToShow = "Cross-Validation (Calibration):\n" + str(arg)
            wx.CallAfter(self.setInfoLable, stringToShow)
        elif msg == "PREDICTION_CHANGED":
            stringToShow = "Current Prediction:\n" + str(arg)
            wx.CallAfter(self.setInfoLable, stringToShow)
        else:
            wx.CallAfter(self.setInfoLable, "Something went wrong!")

    def updatePredictionInfo(self):
        midiEffect = self.controller.programMaster.midiEffectOn
        while self.controller.getLiveSysFromMaster():
            current = self.controller.programMaster.midiEffectOn
            if midiEffect != current:
                stringToShow = "Currently Modulating:\n" + str(current)
                self.infoLabel.SetLabel(stringToShow)
                self.SetSizerAndFit(self.verticalBoxes)
                self.Centre()
                self.Layout()
                midiEffect = current
            time.sleep(1 / (Constants.samplingRate / 2))

    def startButtonPressed(self, event):
        event.Skip()
        if self.startLiveSystemButton.GetLabel() == "Start":
            self.controller.startLiveSystem()
            self.startLiveSystemButton.SetLabel("Stop")
            self.backButton.Enable(False)
        else:
            self.stopLiveSystem()
            self.startLiveSystemButton.SetLabel("Start")
            self.backButton.Enable(True)

    def backButtonPressed(self, event):
        event.Skip()
        self.controller.resetCalibration()
        self.controller.showPanel(self, ChooseCalibrationPanel)

    def stopLiveSystem(self):
        self.controller.stopLiveSystem()

    def quitButtonPressed(self, event):
        event.Skip()
        self.controller.quit()


###########################################################################
# Class ChooseCalibrationPanel
###########################################################################

class ChooseCalibrationPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)

        verticalBoxes = wx.BoxSizer(wx.VERTICAL)
        verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.calibrationLabel = wx.StaticText(self, wx.ID_ANY, u"Calibration", wx.DefaultPosition, wx.DefaultSize,
                                              wx.ALIGN_CENTER_HORIZONTAL)
        self.calibrationLabel.Wrap(-1)
        self.calibrationLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.calibrationLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        verticalBoxes.Add(self.calibrationLabel, 0, wx.EXPAND | wx.ALL, 5)

        verticalBoxes.Add((0, 70), 0, wx.EXPAND, 5)

        self.inbuiltCalibrationButton = wx.Button(self, wx.ID_ANY, "Inbuilt", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.inbuiltCalibrationButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.customCalibrationButton = wx.Button(self, wx.ID_ANY, u"Custom", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.customCalibrationButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.customCalibrationButton.Bind(wx.EVT_BUTTON, self.customCaliPressed)
        self.inbuiltCalibrationButton.Bind(wx.EVT_BUTTON, self.inbuiltCaliPressed)

        self.SetSizerAndFit(verticalBoxes)
        self.Centre()
        self.Layout()

    def customCaliPressed(self, event):
        event.Skip()
        self.controller.showPanel(self, CustomCalibrationPanel, True)

    def inbuiltCaliPressed(self, event):
        event.Skip()
        self.controller.showPanel(self, InbuiltCalibrationPanel, True)


###########################################################################
# Class CustomCalibrationPanel
###########################################################################

class CustomCalibrationPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)

        verticalBoxes = wx.BoxSizer(wx.VERTICAL)
        verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.calibrationLabel = wx.StaticText(self, wx.ID_ANY, u"Calibration", wx.DefaultPosition, wx.DefaultSize,
                                              wx.ALIGN_CENTER_HORIZONTAL)
        self.calibrationLabel.Wrap(-1)
        self.calibrationLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.calibrationLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        verticalBoxes.Add(self.calibrationLabel, 0, wx.EXPAND | wx.ALL, 5)

        verticalBoxes.Add((0, 70), 0, wx.EXPAND, 5)

        self.modTrackButton = wx.Button(self, wx.ID_ANY, "Mod:On", wx.DefaultPosition, wx.DefaultSize, 0)
        self.modTrackButton.Enable(False)
        verticalBoxes.Add(self.modTrackButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.calibrationButton = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.calibrationButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.resetButton = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.resetButton.Enable(False)
        verticalBoxes.Add(self.resetButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        verticalBoxes.Add((0, 50), 1, wx.EXPAND, 5)

        self.calibrationButton.Bind(wx.EVT_BUTTON, self.calibrationButtonPressed)
        self.modTrackButton.Bind(wx.EVT_BUTTON, self.trackModulation)
        self.resetButton.Bind(wx.EVT_BUTTON, self.resetCalibration)
        self.modon = False

        self.SetSizerAndFit(verticalBoxes)
        self.Centre()
        self.Layout()

    # using the button, the beginning and end of the modulation can be tracked
    def trackModulation(self, event):
        event.Skip()
        if self.modon:
            self.controller.endModulation()
            self.modTrackButton.SetLabel("Mod:On")
            self.modon = False
            self.calibrationButton.Enable(True)
        else:
            self.controller.startModulation()
            self.modTrackButton.SetLabel("Mod:Off")
            self.modon = True
            self.calibrationButton.Enable(False)

    def calibrationButtonPressed(self, event):
        event.Skip()
        if self.calibrationButton.GetLabel() == "Start":
            self.controller.startCalibration()
            self.calibrationButton.SetLabel("Stop")
            self.calibrationButton.Enable(False)
            self.resetButton.Enable(True)
            self.modTrackButton.Enable(True)
        else:
            self.controller.endCalibration()
            self.controller.showPanel(self, LiveSystemPanel, True)
            self.calibrationButton.SetLabel("Start")
            self.calibrationButton.Enable(True)
            self.resetButton.Enable(False)
            self.modTrackButton.Enable(False)

    def resetCalibration(self, event):
        event.Skip()
        self.controller.resetCalibration()
        self.calibrationButton.SetLabel("Start")
        self.calibrationButton.Enable(True)
        self.modTrackButton.SetLabel("Mod:On")
        self.modTrackButton.Enable(False)
        self.resetButton.Enable(False)
        self.modon = False


###########################################################################
# Class InbuiltCalibrationPanel
###########################################################################

class InbuiltCalibrationPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)
        self.modTimes = [6000, 8000, 14000, 16000, 22000, 24000, 30000, 32000,
                         38000, 40000, 46000, 48000, 54000, 56000, 62000, 64000]
        self.caliThread = None
        self.isMediaLoaded = False
        self.isVideoPlaying = False

        verticalBoxes = wx.BoxSizer(wx.VERTICAL)

        self.calibrationLabel = wx.StaticText(self, wx.ID_ANY, u"Calibration", wx.DefaultPosition, wx.DefaultSize,
                                              wx.ALIGN_CENTER_HORIZONTAL)
        self.calibrationLabel.Wrap(-1)
        self.calibrationLabel.SetFont(
            wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.calibrationLabel.SetForegroundColour(wx.Colour(17, 133, 49))
        verticalBoxes.Add(self.calibrationLabel, 0, wx.EXPAND | wx.ALL, 5)

        filename = os.path.normpath(os.path.join(os.getcwd(), '..', 'pics/empiano_song.mp4'))
        try:
            self.video = MediaCtrl(self, size=(800, 500))
        except NotImplementedError:
            print("media control not found")

        self.video.Load(filename)
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.mediaLoaded)
        self.video.SetFocus()

        verticalBoxes.Add(self.video, 0, wx.EXPAND, 5)

        hButtonsBox = wx.BoxSizer(wx.HORIZONTAL)

        self.startButton = wx.Button(self, wx.ID_ANY, "Start", wx.DefaultPosition, wx.DefaultSize, 0)
        hButtonsBox.Add(self.startButton, 0, wx.ALL, 5)

        self.resetButton = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        self.resetButton.Enable(False)
        hButtonsBox.Add(self.resetButton, 0, wx.ALL, 5)

        self.finishButton = wx.Button(self, wx.ID_ANY, u"Finish", wx.DefaultPosition, wx.DefaultSize, 0)
        self.finishButton.Enable(False)
        hButtonsBox.Add(self.finishButton, 0, wx.ALL, 5)

        verticalBoxes.Add(hButtonsBox, 0, wx.EXPAND)

        self.startButton.Bind(wx.EVT_BUTTON, self.startButtonPressed)
        self.resetButton.Bind(wx.EVT_BUTTON, self.resetButtonPressed)
        self.finishButton.Bind(wx.EVT_BUTTON, self.finishButtonPressed)

        self.SetSizerAndFit(verticalBoxes)
        self.Centre()
        self.Layout()

    def mediaLoaded(self, event):
        event.Skip()
        self.isMediaLoaded = True

    def startButtonPressed(self, event):
        event.Skip()
        if not self.isMediaLoaded:
            dial = wx.MessageDialog(self, "Sorry, the media did not load, "
                                          "check if the video file exists in the pics folder.",
                                    "Error", wx.OK | wx.STAY_ON_TOP | wx.CENTRE)
            dial.ShowModal()
            return
        self.startButton.Enable(False)
        self.resetButton.Enable(True)
        self.controller.startCalibration()
        self.startVideo()
        self.caliThread = threading.Thread(target=self.trackCalibration)
        self.caliThread.start()

    def startVideo(self):
        self.video.Play()
        self.isVideoPlaying = True

    def trackCalibration(self):
        print("in track Calibration")
        index = 0
        self.Bind(EVT_MEDIA_STOP, self.enableFinishButton)
        while self.isVideoPlaying:
            currentSecond = self.video.Tell()
            if abs(currentSecond - self.modTimes[index]) <= 50:
                if index % 2 == 0:
                    self.controller.startModulation()
                    print("modulation started: ", currentSecond)
                else:
                    self.controller.endModulation()
                    print("modulation ended: ", currentSecond)
                index = index + 1
                if index == len(self.modTimes):
                    break
                print("ein Durchlauf beendet, neuer Index: ", index)

    def enableFinishButton(self, event):
        event.Skip()
        wx.CallAfter(self.finishButton.Enable, True)
        self.isVideoPlaying = False

    def resetButtonPressed(self, event):
        event.Skip()
        self.isVideoPlaying = False
        self.video.Stop()
        self.caliThread.join()
        self.controller.resetCalibration()
        self.startButton.Enable(True)
        self.finishButton.Enable(False)
        self.resetButton.Enable(False)

    def finishButtonPressed(self, event):
        event.Skip()
        self.caliThread.join()
        self.controller.endCalibration()
        self.controller.showPanel(self, LiveSystemPanel, True)
        self.resetPanel()

    def resetPanel(self):
        self.video.Stop()
        self.finishButton.Enable(False)
        self.resetButton.Enable(False)
        self.startButton.Enable(True)



###########################################################################
# Class StreamOverviewPanel
###########################################################################
headers = ["Stream", "Type", "#Channels", "SampleRate", "Format", "hosted on", "source id"]


class StreamOverviewPanel(wx.Panel):
    def __init__(self, parent, controller, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        super(StreamOverviewPanel, self).__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.parent = parent

        self.controller = controller
        if parent.isWindows:
            self.SetBackgroundColour(backgroundColorWindows)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self, size=(800, 500))
        self.grid.EnableEditing(False)
        self.grid.CreateGrid(0, len(headers))
        for i in range(0, len(headers)):
            self.grid.SetColLabelValue(i, headers[i])
        self.grid.SetColFormatNumber(3)
        self.grid.SetColFormatNumber(4)
        self.grid.SetColFormatNumber(5)
        self.grid.Centre()
        self.vbox.Add(self.grid, 0, wx.EXPAND)
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.checkSelectedCell)

        hButtonsBox = wx.BoxSizer(wx.HORIZONTAL)

        self.backButton = wx.Button(self, wx.ID_ANY, "Back", wx.DefaultPosition, wx.DefaultSize, 0)
        hButtonsBox.Add(self.backButton, 0, wx.ALL, 5)

        self.checkStreamsButton = wx.Button(self, wx.ID_ANY, u"Find Streams", wx.DefaultPosition, wx.DefaultSize, 0)
        hButtonsBox.Add(self.checkStreamsButton, 0, wx.ALL, 5)

        self.connectButton = wx.Button(self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0)
        hButtonsBox.Add(self.connectButton, 0, wx.ALL, 5)

        self.vbox.Add(hButtonsBox, 0, wx.EXPAND)
        self.SetSizerAndFit(self.vbox)

        self.backButton.Bind(wx.EVT_BUTTON, self.onBack)
        self.checkStreamsButton.Bind(wx.EVT_BUTTON, self.onUpdateStreams)
        self.connectButton.Bind(wx.EVT_BUTTON, self.connectToStreams)

        self.Centre()
        self.Layout()

    def checkSelectedCell(self, event):
        event.Skip()
        row = event.GetRow()
        selected = self.grid.GetSelectedRows()
        if len(selected) > 1:
            for _row in selected:
                if not row or _row != row:
                    self.grid.DeselectRow(_row)
        self.grid.SelectRow(row)

    def updateStreams(self):
        self.grid.ClearGrid()
        while self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows()
        streams = self.controller.programMaster.streamManager.checkStreamAvailability()
        for streamInfo in streams:
            self.grid.InsertRows()
            self.grid.SetCellValue(0, 0, streamInfo.name())
            self.grid.SetCellValue(0, 1, streamInfo.type())
            self.grid.SetCellValue(0, 2, str(streamInfo.channel_count()))
            self.grid.SetCellValue(0, 3, str(streamInfo.nominal_srate()))
            self.grid.SetCellValue(0, 4, str(streamInfo.channel_format()))
            self.grid.SetCellValue(0, 5, streamInfo.hostname())
            self.grid.SetCellValue(0, 6, streamInfo.uid())
        self.grid.AutoSize()
        self.grid.AutoSizeRows()

    def connectToStreams(self, event):
        event.Skip()
        streams = []
        for i in self.grid.GetSelectedRows():
            streams.append((i, self.grid.GetCellValue(i, 6), float(self.grid.GetCellValue(i, 3)),
                            int(self.grid.GetCellValue(i, 2))))
        if streams:
            threading.Thread(target=pub.subscribe, args=(self.checkIfSuccessful, "streamConnect")).start()
            self.controller.connectToLSLStream(streams)

    def checkIfSuccessful(self, msg, settingsChannels, streamChannels):
        if msg == "CHANNELS_OKAY":
            self.controller.showPanel(self, ChooseCalibrationPanel)
        elif msg == "CHANNELS_TOO_MANY":
            string = "The amount of channels found in the settings  (" + str(settingsChannels) \
                     + ")\n are higher than the channels found in the stream (" \
                     + str(streamChannels) \
                     + ").\n Please correct the settings (channels should be lower or " \
                       "equal to the amount found in the stream)."
            wx.CallAfter(self.showPopup, string, Go_to_settings)
        elif msg == "CHANNELS_TOO_FEW":
            string = "The amount of channels found in the settings  (" + str(settingsChannels) \
                     + ")\n are smaller than the channels found in the stream (" \
                     + str(streamChannels) \
                     + ").\n If that is intended, please continue, otherwise go back to " \
                       "change the settings."
            wx.CallAfter(self.showPopup, string, Continue)
        elif msg == "CONNECT_FAILED":
            string = "The connection to your chosen stream failed, please check if it is still" \
                     " running. Try restarting it, after that you have to click \"Find Streams\" again."
            wx.CallAfter(self.showPopup, string, Back_to_streams)

    def showPopup(self, string, continuePossible):
        if continuePossible == Continue:
            dial = wx.MessageDialog(self, string, "Error", wx.YES_NO | wx.STAY_ON_TOP | wx.CENTRE)
            dial.SetYesNoLabels("&Continue", "&Back")
        else:
            dial = wx.MessageDialog(self, string, "Error", wx.OK | wx.STAY_ON_TOP | wx.CENTRE)
        result = dial.ShowModal()
        if result == wx.ID_YES:
            self.onContinue()
        else:
            if continuePossible == Go_to_settings:
                self.onBackPopUp()

    def onUpdateStreams(self, event):
        event.Skip()
        self.updateStreams()

    def onBack(self, event):
        event.Skip()
        self.controller.showPanel(self, StartPanel)

    def onBackPopUp(self):
        self.controller.resetStream()
        self.parent.backToConnectPage = True
        self.controller.showPanel(self, SettingsPanel)

    def onContinue(self):
        self.controller.setProgramPaused()
        self.controller.showPanel(self, ChooseCalibrationPanel)
