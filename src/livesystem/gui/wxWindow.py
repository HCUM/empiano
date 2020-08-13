# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jul 27 2020)
## http://www.wxformbuilder.org/
###########################################################################

import wx
import wx.xrc
import wx.grid
from threading import Thread
from pubsub import pub

class MyFrame(wx.Frame):
    def __init__(self, controller):
        wx.Frame.__init__(self, None, wx.ID_ANY, title= u"EMPiano",  size = wx.Size( 1000,520 ))
        self.SetSizeHints(wx.Size(1000, 520), wx.DefaultSize)

        self.controller = controller

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.panels = {}
        for panel in (StartPanel, SettingsPanel, InLiveSystemPanel, StartLiveSystemPanel,
                      CalibrationPanel, LSLPanel, StreamOverviewPanel):
            newPanel = panel(self, self.controller)
            self.panels[panel] = newPanel
            newPanel.Hide()
            self.sizer.Add(newPanel, 1, wx.EXPAND)

        panel = self.panels[StartPanel]
        panel.Show()

        self.SetSizer(self.sizer)



###########################################################################
## Class StartPanel
###########################################################################

class StartPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition,
                  size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )


        verticalBoxes.Add( ( 0, 70), 0, wx.EXPAND, 5 )

        self.empianoLabel = wx.StaticText( self, wx.ID_ANY, u"EMPiano", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.empianoLabel.Wrap( -1 )

        self.empianoLabel.SetFont( wx.Font( 60, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial Black" ) )
        self.empianoLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.empianoLabel, 0, wx.ALL|wx.EXPAND, 5 )


        verticalBoxes.Add( ( 0, 70), 0, wx.EXPAND, 5 )

        self.startButton = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.startButton.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )

        verticalBoxes.Add( self.startButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        verticalBoxes.Add( ( 0, 20), 0, wx.EXPAND, 5 )

        self.settingsButton = wx.Button( self, wx.ID_ANY, u"Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.settingsButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        verticalBoxes.Add( ( 0, 20), 0, wx.EXPAND, 5 )

        self.exitButton = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.exitButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.startButton.Bind(wx.EVT_BUTTON, self.showLSLPanel)
        self.settingsButton.Bind(wx.EVT_BUTTON, self.showSettingsPanel)
        self.exitButton.Bind(wx.EVT_BUTTON, self.quitButtonPressed)

        self.SetSizer( verticalBoxes )
        self.Layout()

    def __del__( self ):
        pass

    def showLSLPanel(self, event):
        self.Hide()
        panel = self.Parent.panels[StreamOverviewPanel]
        panel.Show()

    def showSettingsPanel(self, event):
        self.Hide()
        panel = self.Parent.panels[SettingsPanel]
        panel.Show()

    def quitButtonPressed(self, event):
        self.controller.quit()


###########################################################################
## Class SettingsPanel
###########################################################################

class SettingsPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition,
                  size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )

        self.dataAcquisitionLabel = wx.StaticText( self, wx.ID_ANY, u"EMG - Data Acquisition", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dataAcquisitionLabel.Wrap( -1 )

        self.dataAcquisitionLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.dataAcquisitionLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.dataAcquisitionLabel, 0, wx.EXPAND|wx.ALL, 5 )

        flexGridDataAcquisition = wx.FlexGridSizer( 0, 2, 0, 57 )
        flexGridDataAcquisition.AddGrowableCol( 0 )
        flexGridDataAcquisition.AddGrowableCol( 1 )
        flexGridDataAcquisition.SetFlexibleDirection( wx.BOTH )
        flexGridDataAcquisition.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.amtChannelsLabel = wx.StaticText(self, wx.ID_ANY, u"Amount of Electrodes/Channels: ",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.amtChannelsLabel.Wrap(-1)

        flexGridDataAcquisition.Add(self.amtChannelsLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.amtElectrodesInput = wx.TextCtrl(self, wx.ID_ANY, u"8", wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT)

        flexGridDataAcquisition.Add(self.amtElectrodesInput, 0, wx.ALL, 5)


        verticalBoxes.Add( flexGridDataAcquisition, 0, wx.ALL|wx.EXPAND, 5 )

        self.preprocessingLabel = wx.StaticText( self, wx.ID_ANY, u"Preprocessing - Filters",
                                                 wx.DefaultPosition, wx.DefaultSize, 0 )
        self.preprocessingLabel.Wrap( -1 )

        self.preprocessingLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                                  wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.preprocessingLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.preprocessingLabel, 0, wx.ALL, 5 )

        flexGridPreprocessing = wx.FlexGridSizer( 0, 2, 0, 0 )
        flexGridPreprocessing.AddGrowableCol( 0 )
        flexGridPreprocessing.AddGrowableCol( 1 )
        flexGridPreprocessing.SetFlexibleDirection( wx.BOTH )
        flexGridPreprocessing.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lowCutoffBandpassLabel = wx.StaticText(self, wx.ID_ANY, u"Low Cutoff Frequency for Bandpass Filter:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lowCutoffBandpassLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.lowCutoffBandpassLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.lowBandpassInput = wx.TextCtrl(self, wx.ID_ANY, u"2.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.lowBandpassInput, 0, wx.ALL | wx.LEFT, 5)

        self.highCutoffBandpassLabel = wx.StaticText(self, wx.ID_ANY, u"High Cutoff Frequency for Bandpass Filter:\n", wx.DefaultPosition, wx.DefaultSize, 0)
        self.highCutoffBandpassLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.highCutoffBandpassLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.highBandpassInput = wx.TextCtrl(self, wx.ID_ANY, u"100.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.highBandpassInput, 0, wx.ALL, 5)

        self.lowCutoffBandstopLabel = wx.StaticText(self, wx.ID_ANY, u"Low Cutoff Frequency for Bandstop Filter:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.lowCutoffBandstopLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.lowCutoffBandstopLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.lowBandstopInput = wx.TextCtrl(self, wx.ID_ANY, u"49.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.lowBandstopInput, 0, wx.ALL, 5)

        self.highCutoffBandstopLabel = wx.StaticText(self, wx.ID_ANY, u"High Cutoff Frequency for Bandstop Filter:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.highCutoffBandstopLabel.Wrap(-1)

        flexGridPreprocessing.Add(self.highCutoffBandstopLabel, 0, wx.ALL | wx.EXPAND, 5)

        self.highBandstopInput = wx.TextCtrl(self, wx.ID_ANY, u"51.0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridPreprocessing.Add(self.highBandstopInput, 0, wx.ALL, 5)


        verticalBoxes.Add( flexGridPreprocessing, 0, wx.ALL|wx.EXPAND, 5 )

        self.svmSettingsLabel = wx.StaticText( self, wx.ID_ANY, u"SVM - Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.svmSettingsLabel.Wrap( -1 )

        self.svmSettingsLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.svmSettingsLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.svmSettingsLabel, 0, wx.ALL, 5 )

        flexGridSVMSettings = wx.FlexGridSizer( 2, 2, 0, 78 )
        flexGridSVMSettings.AddGrowableCol( 0 )
        flexGridSVMSettings.AddGrowableCol( 1 )
        flexGridSVMSettings.SetFlexibleDirection( wx.BOTH )
        flexGridSVMSettings.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.windowSizeLabel = wx.StaticText( self, wx.ID_ANY, u"Size for Sliding Window (in s):", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.windowSizeLabel.Wrap( -1 )

        flexGridSVMSettings.Add( self.windowSizeLabel, 0, wx.ALL|wx.EXPAND, 5 )

        self.midiCableNameInput = wx.TextCtrl(self, wx.ID_ANY, u"0.15", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY | wx.TE_RIGHT)
        flexGridSVMSettings.Add(self.midiCableNameInput, 0, wx.ALL, 5)

        self.dataValCorrectionLabel = wx.StaticText( self, wx.ID_ANY, u"Value for Correcting the Data:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dataValCorrectionLabel.Wrap( -1 )

        flexGridSVMSettings.Add( self.dataValCorrectionLabel, 0, wx.ALL|wx.EXPAND, 5 )

        self.dataValCorrectionInput = wx.TextCtrl( self, wx.ID_ANY, u"0.000001", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.TE_RIGHT )
        flexGridSVMSettings.Add( self.dataValCorrectionInput, 0, wx.ALL, 5 )


        verticalBoxes.Add( flexGridSVMSettings, 0, wx.ALL|wx.EXPAND, 5 )

        self.midiSettingsLabel = wx.StaticText( self, wx.ID_ANY, u"MIDI - Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.midiSettingsLabel.Wrap( -1 )

        self.midiSettingsLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Lucida Grande" ) )
        self.midiSettingsLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.midiSettingsLabel, 0, wx.ALL, 5 )

        flexGridMidiSettings = wx.FlexGridSizer( 0, 2, 0, 0 )
        flexGridMidiSettings.AddGrowableCol( 1 )
        flexGridMidiSettings.SetFlexibleDirection( wx.BOTH )
        flexGridMidiSettings.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.midiCableName = wx.StaticText( self, wx.ID_ANY, u"Name of the virtual MIDI cable:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.midiCableName.Wrap( -1 )

        flexGridMidiSettings.Add( self.midiCableName, 0, wx.ALL, 5 )

        self.midiCableNameInput = wx.TextCtrl(self, wx.ID_ANY, u"my_midi_cable", wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.TE_RIGHT)
        flexGridMidiSettings.Add(self.midiCableNameInput, 0, wx.ALL | wx.EXPAND, 5)


        verticalBoxes.Add( flexGridMidiSettings, 0, wx.EXPAND|wx.ALL, 5 )

        flexGridCreateCable = wx.FlexGridSizer( 0, 2, 0, 0 )
        flexGridCreateCable.AddGrowableCol( 0 )
        flexGridCreateCable.AddGrowableCol( 1 )
        flexGridCreateCable.SetFlexibleDirection( wx.BOTH )
        flexGridCreateCable.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.createMidiCableLabel = wx.StaticText( self, wx.ID_ANY, u"Create virtual MIDI cable (using mido library):", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.createMidiCableLabel.Wrap( -1 )

        flexGridCreateCable.Add( self.createMidiCableLabel, 0, wx.ALL|wx.EXPAND, 5 )

        self.createMidiCableCheckbox = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.createMidiCableCheckbox.SetValue(True)
        flexGridCreateCable.Add( self.createMidiCableCheckbox, 0, wx.ALL, 5 )


        verticalBoxes.Add( flexGridCreateCable, 0, wx.EXPAND|wx.ALL, 5 )

        self.setSettingsButton = wx.Button( self, wx.ID_ANY, u"Done", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.setSettingsButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        self.SetSizer( verticalBoxes )
        self.Layout()

        # Connect Events
        self.setSettingsButton.Bind( wx.EVT_BUTTON, self.updateSettings )

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def updateSettings(self, event):
        try:
            value = int(self.amtElectrodesInput.GetValue())
            self.controller.updateSettings(value,
                                           self.midiCableNameInput.GetValue(),
                                           self.createMidiCableCheckbox.GetValue())
            self.Hide()
            panel = self.Parent.panels[StartPanel]
            panel.Show()
        except ValueError:
            self.amtElectrodesInput.SetLabel("Insert an integer!")


###########################################################################
## Class InLiveSystemPanel
###########################################################################

class InLiveSystemPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition,
                  size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )

        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.livesystemLabel = wx.StaticText( self, wx.ID_ANY, u"Live-System",
                                              wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.livesystemLabel.Wrap( -1 )

        self.livesystemLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT,
                                               wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.livesystemLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.livesystemLabel, 0, wx.EXPAND|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, 0, 5 )

        self.hintLabel = wx.StaticText( self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.hintLabel.Wrap( -1 )

        self.hintLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.hintLabel.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

        verticalBoxes.Add( self.hintLabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, wx.EXPAND, 5 )

        self.stopLiveSystemButton = wx.Button( self, wx.ID_ANY, u"Stop", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.stopLiveSystemButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.stopLiveSystemButton.Bind(wx.EVT_BUTTON, self.stopLiveSystem)

        self.SetSizer( verticalBoxes )
        self.Layout()

    def __del__( self ):
        pass

    def stopLiveSystem(self, event):
        self.controller.stopLiveSystem()
        self.Hide()
        panel = self.Parent.panels[StartLiveSystemPanel]
        panel.Show()

###########################################################################
## Class StartLiveSystemPanel
###########################################################################

class StartLiveSystemPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )


        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.livesystemLabel = wx.StaticText( self, wx.ID_ANY, u"Live-System", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.livesystemLabel.Wrap( -1 )

        self.livesystemLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.livesystemLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.livesystemLabel, 0, wx.EXPAND|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, wx.EXPAND, 5 )

        self.hintLabel = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.hintLabel.Wrap( -1 )

        self.hintLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.hintLabel.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

        verticalBoxes.Add( self.hintLabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, wx.EXPAND, 5 )

        self.startLiveSystemButton = wx.Button( self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.startLiveSystemButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        self.exitButton = wx.Button( self, wx.ID_ANY, u"Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.exitButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.startLiveSystemButton.Bind(wx.EVT_BUTTON, self.startButtonPressed)
        self.exitButton.Bind(wx.EVT_BUTTON, self.controller.quit)

        self.SetSizer( verticalBoxes )
        self.Layout()

    def __del__( self ):
        pass

    def startButtonPressed(self, event):
        self.controller.startLiveSystem()
        self.Hide()
        panel = self.Parent.panels[InLiveSystemPanel]
        panel.Show()


###########################################################################
## Class LSLPanel
###########################################################################

class LSLPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )

        self.lslConnectLabel = wx.StaticText( self, wx.ID_ANY, u"Connect to your LSL Stream", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.lslConnectLabel.Wrap( -1 )

        self.lslConnectLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.lslConnectLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.lslConnectLabel, 0, wx.EXPAND|wx.TOP, 130 )

        lslInformationGrid = wx.FlexGridSizer( 0, 2, 0, 0 )
        lslInformationGrid.AddGrowableCol( 1 )
        lslInformationGrid.SetFlexibleDirection( wx.BOTH )
        lslInformationGrid.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.optionMenuChoices = [ u"type", u"name" ]
        self.optionMenu = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, self.optionMenuChoices, 0 )
        self.optionMenu.SetSelection( 0 )
        lslInformationGrid.Add( self.optionMenu, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT, 19 )

        self.entry = wx.TextCtrl( self, wx.ID_ANY, u"EEG", wx.DefaultPosition, wx.DefaultSize, 0 )
        lslInformationGrid.Add( self.entry, 0, wx.ALL|wx.EXPAND, 10 )


        verticalBoxes.Add( lslInformationGrid, 0, wx.EXPAND|wx.ALL, 30 )

        self.connectButton = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
        verticalBoxes.Add( self.connectButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( verticalBoxes )
        self.Layout()

        # Connect Events
        self.connectButton.Bind( wx.EVT_BUTTON, self.connectButtonPressed)

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def connectButtonPressed(self, event):
        self.controller.connectToLSLStream(
            self.optionMenuChoices[self.optionMenu.GetSelection()], self.entry.GetValue())
        self.Hide()
        panel = self.Parent.panels[CalibrationPanel]
        panel.Show()


###########################################################################
## Class CalibrationPanel
###########################################################################

class CalibrationPanel ( wx.Panel ):

    def __init__( self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition,
                  size = wx.Size( 430,500 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.controller = controller

        verticalBoxes = wx.BoxSizer( wx.VERTICAL )


        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.calibrationLabel = wx.StaticText( self, wx.ID_ANY, u"Calibration", wx.DefaultPosition,
                                               wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.calibrationLabel.Wrap( -1 )

        self.calibrationLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                                                wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.calibrationLabel.SetForegroundColour( wx.Colour( 17, 133, 49 ) )

        verticalBoxes.Add( self.calibrationLabel, 0, wx.EXPAND|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, wx.EXPAND, 5 )

        self.hintLabel = wx.StaticText( self, wx.ID_ANY, u"Hint: After starting, "
                                                         u"the <Space> key can be used to track the "
                                                         u"ground truth of the sound modultion motion "
                                                         u"for the SVM training. Press it, whenever the "
                                                         u"modulation motion is being started and also when "
                                                         u"it is being ended.", wx.DefaultPosition, wx.DefaultSize,
                                        wx.ALIGN_CENTER_HORIZONTAL )
        self.hintLabel.Wrap( -1 )

        self.hintLabel.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False, "Arial" ) )
        self.hintLabel.SetForegroundColour( wx.Colour( 0, 0, 0 ) )

        verticalBoxes.Add( self.hintLabel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        verticalBoxes.Add( ( 0, 30), 0, wx.EXPAND, 5 )

        self.calibrationButton = wx.Button(self, wx.ID_ANY, u"Start", wx.DefaultPosition, wx.DefaultSize, 0)
        verticalBoxes.Add(self.calibrationButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)


        verticalBoxes.Add( ( 0, 50), 1, wx.EXPAND, 5 )

        self.calibrationButton.Bind(wx.EVT_BUTTON, self.calibrationButtonPressed)

        self.SetSizer( verticalBoxes )
        self.Layout()

    def __del__( self ):
        pass

    def calibrationButtonPressed(self, event):
        if self.calibrationButton.GetLabel() == "Start":
            self.controller.startCalibration()
            self.calibrationButton.SetLabel("Stop")
        else:
            self.controller.endCalibration()
            self.Hide()
            panel = self.Parent.panels[StartLiveSystemPanel]
            panel.Show()


headers = ["Stream", "Type", "#Channels", "SampleRate", "Format", "hosted on", "source id", "Time offset", "Status"]

class StreamOverviewPanel(wx.Panel):

    def __init__(self, parent, controller, id = wx.ID_ANY, pos = wx.DefaultPosition,
                  size = wx.Size(800,500), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        super(StreamOverviewPanel, self).__init__(parent, id = id, pos = pos, size = size, style = style, name = name )
        self.parent = parent
        self.controller = controller

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)
        self.grid.EnableEditing(True)
        self.grid.CreateGrid(0,len(headers))
        for i in range(0, len(headers)):
            self.grid.SetColLabelValue(i, headers[i])
        self.grid.SetColFormatNumber(3)
        self.grid.SetColFormatNumber(4)
        self.grid.SetColFormatNumber(5)
        self.grid.SetColFormatFloat(8)

        szr = wx.BoxSizer(wx.VERTICAL)
        szr.Add(self.grid, 0, wx.EXPAND)
        self.SetSizer(szr)

        self.makeMenuBar()
        self.parent.CreateStatusBar()
        self.parent.SetStatusText("Idle")

    def updateStreams(self):
        self.grid.ClearGrid()
        while self.grid.GetNumberRows() > 0:
            self.grid.DeleteRows()
        streams = self.controller.checkStreamAvailability()
        for streamInfo in streams:
            self.grid.InsertRows()
            self.grid.SetCellValue(0, 0, streamInfo.name())
            self.grid.SetCellValue(0, 1, streamInfo.type())
            self.grid.SetCellValue(0, 2, str(streamInfo.channel_count()))
            self.grid.SetCellValue(0, 3, str(streamInfo.nominal_srate()))
            self.grid.SetCellValue(0, 4, str(streamInfo.channel_format()))
            self.grid.SetCellValue(0, 5, streamInfo.hostname())
            self.grid.SetCellValue(0, 6, streamInfo.uid())
            self.grid.SetCellValue(0, 7, "N/A")
            self.grid.SetCellValue(0, 8, "Disconnected")
        self.grid.AutoSize()

    def connectToStreams(self):
        uids = []
        for i in self.grid.GetSelectedRows():
            uids.append((i, self.grid.GetCellValue(i, 6)))
        streams = self.controller.connectToLSLStream()
        for i in range(0, self.grid.GetNumberRows()):
            self.grid.SetCellValue(i, 7, "N/A")
            self.grid.SetCellValue(i, 8, "Disconnected")
        for (rowid, inlets, timeCorrection) in streams:
            self.grid.SetCellValue(rowid, 7, str(timeCorrection))
            self.grid.SetCellValue(rowid, 8, "Connected")
        self.grid.AutoSize()
        self.parent.SetStatusText("Idle")


    def makeMenuBar(self):
        fileMenu = wx.Menu()

        checkStreamsItem = fileMenu.Append(-1, "&Check streams \tCtrl-H", "Checking the network for all available LSL streams")
        connectStreamsItem = fileMenu.Append(-1, "&Connect streams \tCtrl-J", "Connecting to marked streams")

        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.parent.SetMenuBar(menuBar)

        self.parent.Bind(wx.EVT_MENU, self.OnUpdateStreams, checkStreamsItem)
        self.parent.Bind(wx.EVT_MENU, self.OnConnectStreams, connectStreamsItem)

        self.parent.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.parent.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

        pub.subscribe(self.UpdateStatusBar, "streamManager")


    def OnUpdateStreams(self, event):
        self.parent.SetStatusText("Looking for streams...")
        self.updateStreams()
        self.parent.SetStatusText("Idle")

    def OnConnectStreams(self, event):
        self.parent.SetStatusText("Connecting to streams...")
        ConnectStreamsTask(self)

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        wx.MessageBox("This is a wxPython Hello World sample", "About Hello World 2", wx.OK | wx.ICON_INFORMATION)

    def UpdateStatusBar(self, msg):
        if msg=="CONNECT_SUCCESS":
            self.parent.SetStatusText("Idle")
        elif msg=="RECORD_STOP":
            self.parent.SetStatusText("Idle")
        else:
            self.parent.SetStatusText("Something went wrong!")


class ConnectStreamsTask(Thread):
    def __init__(self, panel):
        Thread.__init__(self)
        self.panel = panel
        self.start()

    def run(self):
        self.panel.connectToStreams()
        wx.CallAfter(pub.sendMessage, "streamManager", msg="CONNECT_SUCCESS")

