from pylsl import ContinuousResolver, StreamInlet, resolve_stream
import storage.Constants as constants


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

    # Initializes the connection to the defined LSL-stream
    def connectStreams(self, streams):
        #disconnect all other streams
        self.inlets = []
        #connect to streams given their uids
        for (rowid, uid, samplingRate) in streams:
            streams = resolve_stream('uid', uid)
            inlet = StreamInlet(streams[0])
            self.inlets.append((rowid, inlet, inlet.time_correction(), samplingRate))
        if self.inlets:
            self.stream = self.inlets[0]
            self.streamInlet = self.stream[1]
            constants.samplingRate = self.stream[3]

    # Pulls samples from the LSL-stream, without saving them.
    # Needed for the times outside of the calibration and livesystem
    # -> buffer needs to be kept empty
    def keepPullingSamplesFromInlet(self):
        self.streamInlet.pull_sample()
