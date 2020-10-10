import scipy.signal as signal
import storage.Constants as Constants


def butter_bandstop_filter(data, cutoff_low, cutoff_high, nyq_freq, order=3):
    sos = signal.butter(order, [cutoff_low / nyq_freq, cutoff_high / nyq_freq], btype='bandstop', output='sos')
    y = signal.sosfiltfilt(sos, data)
    return y


def butter_bandpass_filter(data, cutoff_low, cutoff_high, nyq_freq, order=3):
    sos = signal.butter(order, [cutoff_low / nyq_freq, cutoff_high / nyq_freq], btype='bandpass', output='sos')
    y = signal.sosfiltfilt(sos, data)
    return y


# applies a bandstop and bandpass filter to all the channels of the data
def performPreprocessing(rawData):
    bandStopData = []
    for channel in rawData:
        # apply filters
        bandChannelData = butter_bandpass_filter(channel, Constants.lowerBoundCutOutFreq,
                                                 Constants.upperBoundCutOutFreq, Constants.samplingRate * 0.5)

        bandStopData.append(butter_bandstop_filter(bandChannelData, Constants.lowBandStopFreq,
                                                   Constants.highBandStopFreq, Constants.samplingRate * 0.5))
    return bandStopData
