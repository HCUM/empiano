import livesystem.midiManager as midimanager
import mido
import time

def main():
    midiManager = midimanager.MidiManager(None)
    #metaMsg = mido.MetaMessage('piano')
    #midiManager.sendMidiMsg(metaMsg)
    programChange = mido.Message('program_change',program=11, time=0)
    midiManager.sendMidiMsg(programChange)
    i = 60
    while i <= 127:
        midiManager.outport.panic()
        msg = mido.Message('note_on', note=i)
        print("this message is sent: ", msg)
        midiManager.sendMidiMsg(msg)
        i += 1
        time.sleep(1)

def newMain():
    outport = mido.open_output('IAC-Treiber Bus 1')
    with mido.open_input('USB MIDI Interface') as inport:
        for msg in inport:
            outport.send(msg)

if __name__ == '__main__':
    newMain()