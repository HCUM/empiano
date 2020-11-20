# for data acquisition:
numberOfChannels = 8
samplingRate = 500.0

# for preprocessing:
lowBandPassFreq = 2.0
highBandPassFreq = 100.0
lowBandStopFreq = 49
highBandStopFreq = 51

# for feature calculation:
windowSize = 0.15  # in s -> 150ms = 0.15s
samplesPerWindow = int(windowSize / (1. / samplingRate))
windowShift = int(samplesPerWindow / 2)
dataSampleCorrection = 0.000001

# virtual midi cable:
virtualMIDICable = 'my_midi_cable'
createMIDICable = True
