import mido
import time
from storage import Constants as constants

###########################################################################
## Class CalibrationManager
## -> manages all the midi-related things
###########################################################################
class MidiManager:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.output = None
        self.pitchValues = [0, 250, 500, 1000, 500, 250,  0, -250, -500, -1000, -500, -250]


    #Creates either a virtual MIDI cable or builds a connection to an existing virtual MIDI cable
    def createMIDIOutport(self):
        if constants.createMIDICable:
            self.output = mido.open_output(constants.virtualMIDICable, virtual=True)
        else:
            names = mido.get_output_names()
            for name in names:
                if name.startswith(constants.virtualMIDICable):
                    self.output = mido.open_output(name)

    # Looks for the virtual midi-cable with the given name
    # This is needed, because sometimes the index of the virtual cable is added to the name,
    # which cannot be known by the user
    def findMidiCable(self, midiCableName):
        names = mido.get_output_names()
        for name in names:
            if name.startswith(midiCableName):
                return True, name
        return False, midiCableName

    # Method is called whenever the system predicted an augmentation;
    # Constantly sends pitchwheel midi-messages with different pitch values (specified in self.pitchValues);
    # These are sent to a virtual midi cable (specified in self.outport)
    def sendEffect(self):
        index = 0
        while(self.programMaster.midiEffectOn):
            self.sendMidiMsg(
                mido.Message('pitchwheel', channel=0, pitch=self.pitchValues[index%len(self.pitchValues)]))
            index += 1
            time.sleep(1/8/len(self.pitchValues))

        #resets the pitchwheel value
        self.sendMidiMsg(mido.Message('pitchwheel', channel=0, pitch=0))

    # Sends the reset pitchwheel midi-message
    def sendPitchWheelStopMsg(self):
        self.sendMidiMsg(mido.Message('pitchwheel', channel=0, pitch=0))

    def sendMidiMsg(self, msg):
        self.output.send(msg)