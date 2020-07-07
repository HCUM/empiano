import time
import numpy as np
from workers import RecordingsManager
from pylsl import StreamInfo, StreamOutlet, pylsl

def createDataStream():
    #name: BioSemi; content-type: EEG; channels: 8; Hz: 500; value of data: float; unique id: id1
    info = StreamInfo("EMG-data", 'EEG', 12, 500, 'float32', 'id1')
    return StreamOutlet(info)


def sendData(outlet, data):
    print("start sending data")
    i = 0
    data = np.asarray(data)
    while i < len(data[0]):
        outlet.push_sample(x=data[:,i], timestamp=pylsl.local_clock())
        #print("data sent: ", data[:, i])
        i += 1
        time.sleep(0.002)
    print("finished sending data")

def sendLiveData(outlet, data):
    #time.sleep(1)
    for (sample, timestamp) in data:
        outlet.push_sample(x=sample, timestamp=timestamp)
        #print("sample sent: ", sample)
        #time.sleep(0.002)
    while True:
        outlet.push_sample(x=[0 for i in range(12)], timestamp=0)
    #time.sleep(3)

def sendTestData(outlet, data):
    print("start sending data")
    for sample in data:
        outlet.push_sample(sample)
        time.sleep(0.1)
    print("finished sending data")

def main():
    print("starting sender")
    data, _ = RecordingsManager.getDataAndMarkersCsv("2019-08-08_20.31.22_livesystemRound1DataTimestamps", "2019-08-08_20.31.25_livesystemRound1TimestampMarker")
    outlet = createDataStream()
    sendLiveData(outlet, data)
    print("stopping sender")

def testMethod(outlet, data):
    sendTestData(outlet, data)