import mido
import time
import logging

# manages all the midi-related things
class MidiManager:

    def __init__(self, programMaster):
        self.logger = logging.getLogger()
        self.programMaster = programMaster
        self.outport = mido.open_output('IAC-Treiber IAC-Bus 1')  #input could be needed for the piano: port = 'USB MIDI Interface'
        self.pitchValues = [0, 250, 500, 1000, 500, 250,  0, -250, -500, -1000, -500, -250]


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
        #self.logger.info("MIDI-Manager: Message sent: %s", msg)