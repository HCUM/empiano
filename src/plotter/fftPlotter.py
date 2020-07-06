from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt

def plotFFT(data):
    fig, axs = plt.subplots(len(data), sharex=True)
    for ax, channel in zip(axs.flat, data):
        channelData = np.asarray(channel)
        fftData = fft(channelData)
        ax.plot(fftData)
    #plt.show()
