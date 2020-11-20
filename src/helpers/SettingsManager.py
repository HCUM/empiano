import os
import configparser
import storage.Constants as Constants


# Writes the settings of the user into a file
def writeConfigFile():
    config = configparser.ConfigParser()
    config['STREAM'] = {'amtChannels': str(Constants.numberOfChannels)}
    config['FILTER'] = {'lowBandPassFreq': str(Constants.lowBandPassFreq),
                        'highBandPassFreq': str(Constants.highBandPassFreq),
                        'lowBandStopFreq': str(Constants.lowBandStopFreq),
                        'highBandStopFreq': str(Constants.highBandStopFreq)}
    config['SVM'] = {'windowSize': str(Constants.windowSize)}
    config['MIDI'] = {'create': str(Constants.createMIDICable),
                      'name': str(Constants.virtualMIDICable)}
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    with open(path, 'w') as configfile:
        config.write(configfile)


# Updates the fields in Constants.py, like the user changed them in the settings
def updateAllSettings(amtChannels, lowBandPassFreq, highBandPassFreq, lowBandStopFreq, highBandStopFreq, windowSize,
                      midiCableName, shouldCreateMidiCable):

    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    noChanges = Constants.lowBandPassFreq == lowBandPassFreq and noChanges
    Constants.lowBandPassFreq = float(lowBandPassFreq)

    noChanges = Constants.highBandPassFreq == highBandPassFreq and noChanges
    Constants.highBandPassFreq = float(highBandPassFreq)

    noChanges = Constants.lowBandStopFreq == lowBandStopFreq and noChanges
    Constants.lowBandStopFreq = lowBandStopFreq

    noChanges = Constants.highBandStopFreq == highBandStopFreq and noChanges
    Constants.highBandStopFreq = highBandStopFreq

    noChanges = Constants.windowSize == windowSize and noChanges
    Constants.windowSize = windowSize

    noChanges = Constants.virtualMIDICable == midiCableName and noChanges
    Constants.virtualMIDICable = midiCableName

    noChanges = Constants.createMIDICable == shouldCreateMidiCable and noChanges
    Constants.createMIDICable = shouldCreateMidiCable

    if not noChanges:
        writeConfigFile()


# Updates the changed numberOfChannels field in Constants.py
def updateChannelSettings(amtChannels, lowBandPassFreq, highBandPassFreq, lowBandStopFreq,
                          highBandStopFreq, windowSize):
    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    noChanges = Constants.lowBandPassFreq == lowBandPassFreq and noChanges
    Constants.lowBandPassFreq = float(lowBandPassFreq)

    noChanges = Constants.highBandPassFreq == highBandPassFreq and noChanges
    Constants.highBandPassFreq = float(highBandPassFreq)

    noChanges = Constants.lowBandStopFreq == lowBandStopFreq and noChanges
    Constants.lowBandStopFreq = lowBandStopFreq

    noChanges = Constants.highBandStopFreq == highBandStopFreq and noChanges
    Constants.highBandStopFreq = highBandStopFreq

    noChanges = Constants.windowSize == windowSize and noChanges
    Constants.windowSize = windowSize

    if not noChanges:
        writeConfigFile()


# reads the config file and saves the values to the corresponding fields in Constants.py
def readConfigFile():
    config = configparser.ConfigParser()
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    if config.read(path):
        Constants.numberOfChannels = int(config['STREAM']['amtChannels'])
        Constants.lowBandPassFreq = float(config['FILTER']['lowBandPassFreq'])
        Constants.highBandPassFreq = float(config['FILTER']['highBandPassFreq'])
        Constants.lowBandStopFreq = int(config['FILTER']['lowBandStopFreq'])
        Constants.highBandStopFreq = int(config['FILTER']['highBandStopFreq'])
        Constants.windowSize = float(config['SVM']['windowSize'])
        Constants.virtualMIDICable = config['MIDI']['name']
        Constants.createMIDICable = config['MIDI'].getboolean('create')


# resets all the settings made by the user back to the "factory settings"
def resetToFactorySettings():
    updateAllSettings(8, 2.0, 100.0, 49, 51, 0.15, 'my_midi_cable', True)
