from pylsl import ContinuousResolver, StreamInlet, resolve_stream, local_clock
from threading import Thread, get_ident
import pickle
from datetime import datetime


class StreamManager:

    def __init__(self):
        self.resolver = ContinuousResolver()
        self.inlets = []
        self.recordingThreads = []
        self.pathname = "."

    def checkStreamAvailability(self):
        return self.resolver.results()

    def connectStreams(self, uids):
        #disconnect all other streams
        self.inlets = []
        #connect to streams given their uids
        for (rowid, uid) in uids:
            streams = resolve_stream('uid', uid)
            inlet = StreamInlet(streams[0])
            time_correction = inlet.time_correction()
            self.inlets.append((rowid, inlet, time_correction))
        return self.inlets

    def startRecordingFromStreams(self, pathname):
        self.pathname = pathname
        print(pathname)
        self.timeLastRecording = local_clock()
        self.startDateOfRecording = str(datetime.now())
        #start a recording thread for every stream
        for inlet in self.inlets:
            recordThread = RecordThread(inlet[1], self)
            self.recordingThreads.append(recordThread)
            recordThread.start()

    def stopRecordingFromStreams(self):
        durationRecording = local_clock() - self.timeLastRecording
        file = open(self.pathname + "/" +  str(datetime.now()).replace(":", ".").replace(" ", "_") + ".txt", 'w')
        file.write("Start of recording: " + self.startDateOfRecording + "\n")
        file.write("End of recording: " + str(datetime.now()) + "\n")
        file.write("Duration of recording (LSL measured): " + str(durationRecording) + " (ca. " + "{0:.1f}".format(durationRecording/60.0) + " min)\n")
        file.write("Streams:\n")
        file.write("name\ttype\tchannel_count\tsample_rate\tformat\thost\tuid\ttime_correction\tsource_id\tversion\tcreated_at\n")
        for thread in self.recordingThreads:
            thread.running = False
            thread.join()
            #save info to recordings file
            info = thread.inlet.info()
            file.write(str(info.name()) + "\t" + str(info.type()) + "\t" + str(info.channel_count()) + "\t" + str(info.nominal_srate()) + "\t" + str(info.channel_format()) + "\t" + str(info.hostname()) + "\t"
                       + str(info.uid()) + "\t" + str(thread.timeCorrection) + "\t" + str(info.source_id()) + "\t" + str(info.version()) + "\t" + str(info.created_at()) + "\n")
        self.recordingThreads = []


class RecordThread(Thread):

    def __init__(self, inlet, streamManager):
        Thread.__init__(self)
        self.streamManager = streamManager
        self.running=False
        self.inlet = inlet
        self.data = []
        self.timeCorrection = inlet.time_correction()

    def run(self):
        self.running=True
        while self.running:
            sample, ts = self.inlet.pull_sample(timeout=10.0)
            if ts is not None:
                ts += self.timeCorrection
                self.data.append((ts, sample))

        #wait for running to change to False, then save all data
        pickle.dump(self.data, open(self.streamManager.pathname + "/" + str(self.inlet.info().name()) + "_" + str(get_ident()) + ".p", 'wb'))
