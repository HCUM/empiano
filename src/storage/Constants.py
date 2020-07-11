# noinspection PyPep8

samplingRate         = 500.0
lowerBoundCutOutFreq = 2.0
upperBoundCutOutFreq = 100.0
lowBandStopFreq      = 49
highBandStopFreq     = 51
numberOfChannels     = 8
windowSize           = 0.15 #in s -> 150ms = 0.15s -> our sampling rate = 500Hz-> one sample every 0.002s
samplesPerWindow     = int(windowSize / (1. / samplingRate))
windowShift          = int(samplesPerWindow / 2)
lowestValidChannel   = 0
highestValidChannel  = 7
dataSampleCorrection = 0.000001
#for study
savePath             = "./log/"

