import os
import configparser
import storage.Constants as Constants


# Writes the settings of the user into a file
def writeConfigFile():
    config = configparser.ConfigParser()
    config['STREAM'] = {'amtChannels': str(Constants.numberOfChannels)}
    config['MIDI'] = {'create': str(Constants.createMIDICable),
                      'name': str(Constants.virtualMIDICable)}
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    with open(path, 'w') as configfile:
        config.write(configfile)


# Updates the fields in Constants.py, like the user changed them in the settings
def updateSettings(amtChannels, midiCableName, shouldCreateMidiCable):

    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    noChanges = Constants.virtualMIDICable == midiCableName and noChanges
    Constants.virtualMIDICable = midiCableName

    noChanges = Constants.createMIDICable == shouldCreateMidiCable and noChanges
    Constants.createMIDICable = shouldCreateMidiCable

    if not noChanges:
        writeConfigFile()


# Updates the changed numberOfChannels field in Constants.py
def updateChannelSettings(amtChannels):
    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    if not noChanges:
        writeConfigFile()


# reads the config file and saves the values to the corresponding fields in Constants.py
def readConfigFile():
    config = configparser.ConfigParser()
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    if config.read(path):
        Constants.numberOfChannels = int(config['STREAM']['amtChannels'])
        Constants.virtualMIDICable = config['MIDI']['name']
        Constants.createMIDICable = config['MIDI'].getboolean('create')
