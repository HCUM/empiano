import mido
import time
from storage import Constants as constants

# manages all the midi-related things
class MidiManager:

    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.outport:mido.ports
        self.pitchValues = [0, 250, 500, 1000, 500, 250,  0, -250, -500, -1000, -500, -250]


    #creates either a virtual MIDI cable or builds a connection to an existing virtual MIDI cable
    def createMIDIOutport(self):
        if constants.createMIDICable:
            self.outport = mido.open_output(constants.virtualMIDICable, virtual=True)
        else:
            self.outport = mido.open_output(constants.virtualMIDICable)


    # method is called whenever the system predicted an augmentation;
    # constantly send pitchwheel midi-messages with different pitch values (specified in self.pitchValues);
    # messages are sent to a virtual midi cable (specified in self.outport);
    def sendEffect(self):
        index = 0
        while(self.programMaster.midiEffectOn):
            self.sendMidiMsg(
                mido.Message('pitchwheel', channel=0, pitch=self.pitchValues[index%len(self.pitchValues)]))
            index += 1
            time.sleep(1/8/len(self.pitchValues))

        #resets the pitchwheel value
        self.sendMidiMsg(mido.Message('pitchwheel', channel=0, pitch=0))

    # sends the reset pitchwheel midi-message
    def sendPitchWheelStopMsg(self):
        self.sendMidiMsg(mido.Message('pitchwheel', channel=0, pitch=0))

    def sendMidiMsg(self, msg):
        self.outport.send(msg)