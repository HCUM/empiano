from pylsl import ContinuousResolver, StreamInlet, resolve_stream, local_clock
from threading import Thread, get_ident
from datetime import datetime
import pickle


class StreamManager:

    def __init__(self):
        self.resolver = ContinuousResolver()
        self.inlets = []
        self.recordingThreads = []
        self.pathname = "."
        self.stream = ()
        self.streamInlet: StreamInlet

    def checkStreamAvailability(self):
        results = self.resolver.results()
        return results

    def connectStreams(self, uids):
        #disconnect all other streams
        self.inlets = []
        #connect to streams given their uids
        for (rowid, uid) in uids:
            streams = resolve_stream('uid', uid)
            inlet = StreamInlet(streams[0])
            self.inlets.append((rowid, inlet, inlet.time_correction()))
        if self.inlets:
            self.stream = self.inlets[0]
            self.streamInlet = self.stream[1]

    def keepPullingSamplesFromInlet(self):
        self.streamInlet.pull_sample()
