# for data acquisition:
numberOfChannels     = 8
samplingRate         = 500.0
# for preprocessing:
lowerBoundCutOutFreq = 2.0
upperBoundCutOutFreq = 100.0
lowBandStopFreq      = 49
highBandStopFreq     = 51
# for feature calculation:
windowSize           = 0.15 #in s -> 150ms = 0.15s -> our sampling rate = 500Hz-> one sample every 0.002s
samplesPerWindow     = int(windowSize / (1. / samplingRate))
windowShift          = int(samplesPerWindow / 2)
dataSampleCorrection = 0.000001
# virtual midi cable:
virtualMIDICable = 'IAC-Treiber IAC-Bus 1'
createMIDICable  = True

