from scipy.signal import butter, lfilter
import scipy.signal as signal
import storage.Constants as constants


def butter_bandstop_filter(data, cutoff_low, cutoff_high, nyq_freq, order=3):
    sos = signal.butter(order, [cutoff_low / nyq_freq, cutoff_high / nyq_freq], btype='bandstop', output='sos')
    y = signal.sosfiltfilt(sos, data)
    return y

def butter_bandpass_filter(data, cutoff_low, cutoff_high, nyq_freq, order=3):
    sos = signal.butter(order, [cutoff_low / nyq_freq, cutoff_high / nyq_freq], btype='bandpass', output='sos')
    y = signal.sosfiltfilt(sos, data)
    return y


def butter_band(lowcut_param, highcut_param, fs_param, type, order=5):
    nyq  = 0.5 * fs_param
    low  = lowcut_param / nyq
    high = highcut_param / nyq
    b, a = butter(order, [low, high], btype=type)
    return b, a


def butter_band_filter(data, lowcut_param, highcut_param, fs_param, type, order=5):
    b, a = butter_band(lowcut_param, highcut_param, fs_param, type, order=order)
    y    = lfilter(b, a, data)
    return y

# applies a bandstop and bandpass filter to all the channels of the data
def performPreprocessing(rawData):
    bandStopData = []
    for channel in rawData:
        # apply filters
        bandChannelData = butter_bandpass_filter(channel, constants.lowerBoundCutOutFreq,
                               constants.upperBoundCutOutFreq, constants.samplingRate * 0.5)

        #butter_band_filter(channel, constants.lowerBoundCutOutFreq,
        #                       constants.upperBoundCutOutFreq, constants.samplingRate, 'band')

        bandStopData.append(butter_bandstop_filter(bandChannelData, constants.lowBandStopFreq,
                               constants.highBandStopFreq, constants.samplingRate * 0.5))

#            butter_band_filter(bandChannelData, constants.lowBandStopFreq,
#                               constants.highBandStopFreq, constants.samplingRate, 'bandstop'))

    return bandStopData