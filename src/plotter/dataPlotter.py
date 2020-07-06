import matplotlib.pyplot as plt
import numpy as np
import datetime
from storage import constants
from workers import preprocessor

def plotDataWithTimestamps(data, mods):
    #print("in the plot timestamps method")
    colors = ["black", "purple", "blue", "green", "yellow", "orange", "red", "grey"]
    timestamps = [tmstmp for (smp, tmstmp) in data]

    for i in range(constants.numberOfChannels):
        plt.plot(timestamps, [smp[i] for (smp, tmstmp) in data])
        for mod in mods:
            plt.axvline(x=mod[0], color="red", linewidth=0.1)
            plt.axvline(x=mod[1], color="red", linewidth=0.1)

        plt.show()

def plotData(eegData, mods):
    i = 0
    for channel in eegData:
        i+=1
        plt.figure(figsize=(15,5))
        plt.plot(channel)
        plt.title("Channel " + str(i))
        for mod in mods:
            plt.axvline(x=mod[0], color="red", linewidth=0.1)
            plt.axvline(x=mod[1], color="red", linewidth=0.1)

        plt.show()

def plotCaliData(data, mods):
    preprocessedData = preprocessor.performPreprocessing(data)
    x = 1
    for channel in preprocessedData:
        channelData = np.asarray(channel)
        plt.plot(channelData)
        for mod in mods:
            plt.axvline(x=mod[0], color="red", linewidth=0.1)
            plt.axvline(x=mod[1], color="red", linewidth=0.1)

        now = datetime.datetime.now()
        name = now.strftime("%Y-%m-%d %H.%M.%S_") + 'CaliData'+'Channel'+str(x)
        path = "./plots/dataLiveSystem/" + name + ".png"
        plt.savefig(path)
        plt.show()
        x+=1

class LivePlotter:
    def __init__(self):
        #self.fig, self.axs = plt.subplots(constants.numberOfChannels, sharex=True)
        self.data = [[] for i in range(constants.numberOfChannels)]

    def addSample(self, sample):
        for channel, value in zip(self.data, sample):
            channel.append(value)


    def finishPlot(self):
        preprocessedData = preprocessor.performPreprocessing(self.data)
        x = 1
        for channel in preprocessedData:
            plt.plot(channel)
            now = datetime.datetime.now()
            name = now.strftime("%Y-%m-%d %H.%M.%S_") + 'LiveDataChannel' + str(x)
            path = "./plots/dataLiveSystem/" + name + ".png"
            plt.savefig(path)
            plt.show()
            x+=1

