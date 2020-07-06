from scipy.signal import butter, lfilter
import storage.constants as constants


def bandpassAllChannels(eegDf, lowcutParam=constants.lowerBoundCutOutFreq,
                        highcutParam=constants.upperBoundCutOutFreq, fsParam=constants.samplingRate):
    for i in range(constants.numberOfChannels):
        eegDf[i] = butter_band_filter(eegDf[i], lowcutParam, highcutParam, fsParam, 'band')


def bandStopAllChannels(eegDf, lowParam=constants.lowBandStopFreq,
                        highParam=constants.highBandStopFreq, fsParam=constants.samplingRate):
    for i in range(constants.numberOfChannels):
        eegDf[i] = butter_band_filter(eegDf[i], lowParam, highParam, fsParam, 'bandstop')


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

def performPreprocessing(rawData):
    bandStopData = []
    for channel in rawData:
        # apply filters
        bandChannelData = butter_band_filter(channel, constants.lowerBoundCutOutFreq,
                               constants.upperBoundCutOutFreq, constants.samplingRate, 'band')

        bandStopData.append(
            butter_band_filter(bandChannelData, constants.lowBandStopFreq,
                               constants.highBandStopFreq, constants.samplingRate, 'bandstop'))

    return bandStopData