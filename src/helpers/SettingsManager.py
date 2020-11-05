import storage.Constants as Constants
import configparser
import os


def writeConfigFile():
    config = configparser.ConfigParser()
    config['STREAM'] = {'amtChannels': str(Constants.numberOfChannels)}
    config['MIDI'] = {'create': str(Constants.createMIDICable),
                      'name': str(Constants.virtualMIDICable)}
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    with open(path, 'w') as configfile:
        config.write(configfile)


# Updates the values changed in the settings
def updateSettings(amtChannels, midiCableName, shouldCreateMidiCable):

    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    noChanges = Constants.virtualMIDICable == midiCableName and noChanges
    Constants.virtualMIDICable = midiCableName

    noChanges = Constants.createMIDICable == shouldCreateMidiCable and noChanges
    Constants.createMIDICable = shouldCreateMidiCable

    if not noChanges:
        writeConfigFile()

def updateChannelSettings(amtChannels):
    noChanges = Constants.numberOfChannels == amtChannels
    Constants.numberOfChannels = amtChannels

    if not noChanges:
        writeConfigFile()



def readConfigFile():
    config = configparser.ConfigParser()
    path = os.path.normpath(os.path.join(os.getcwd(), 'storage/settings.ini'))
    if config.read(path):
        Constants.numberOfChannels = int(config['STREAM']['amtChannels'])
        Constants.virtualMIDICable = config['MIDI']['name']
        Constants.createMIDICable = config['MIDI'].getboolean('create')
