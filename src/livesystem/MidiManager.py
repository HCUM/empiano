import mido
import time
import logging

class MidiManager:

    def __init__(self, programMaster):
        self.logger = logging.getLogger()
        self.programMaster = programMaster
        self.outport = mido.open_output('IAC-Treiber IAC-Bus 1')  #input could be needed for the piano: port = 'USB MIDI Interface'
        self.pitchValues = [0, 250, 500, 1000, 500, 250,  0, -250, -500, -1000, -500, -250]


    def sendEffect(self):
        index = 0
        while(self.programMaster.midiEffectOn):
            self.sendMidiMsg(
                mido.Message('pitchwheel', channel=0, pitch=self.pitchValues[index%len(self.pitchValues)]))
            index += 1
            time.sleep(1/8/len(self.pitchValues))

        self.sendMidiMsg(
            mido.Message('pitchwheel', channel=0, pitch=0))

    def sendPitchWheelStopMsg(self):
        self.sendMidiMsg(mido.Message('pitchwheel', channel=0, pitch=0))

    def sendMidiMsg(self, msg):
        self.outport.send(msg)
        #self.logger.info("MIDI-Manager: Message sent: %s", msg)