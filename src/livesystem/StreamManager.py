import pylsl
from pubsub import pub
import storage.Constants as Constants
from pylsl import ContinuousResolver, StreamInlet, resolve_byprop


class StreamManager:
    def __init__(self, programMaster):
        self.programMaster = programMaster
        self.resolver = ContinuousResolver()
        self.stream = ()
        self.streamInlet = None

    def checkStreamAvailability(self):
        results = self.resolver.results()
        return results

    # Resets the LSL-stream
    def resetStream(self):
        self.stream = ()
        self.streamInlet = None

    # Initializes the connection to the defined LSL-stream
    def connectStreams(self, streams):
        # connect to streams given their uids
        _, uid, samplingRate, amtChannels = streams[0]
        stream = resolve_byprop('uid', uid, timeout=5)
        if stream:
            self.streamInlet = StreamInlet(stream[0])
            if amtChannels == Constants.numberOfChannels:
                Constants.samplingRate = samplingRate
                pub.sendMessage("streamConnect", msg="CHANNELS_OKAY", settingsChannels=Constants.numberOfChannels,
                                streamChannels=amtChannels)
            elif amtChannels < Constants.numberOfChannels:
                self.resetStream()
                pub.sendMessage("streamConnect", msg="CHANNELS_TOO_MANY", settingsChannels=Constants.numberOfChannels,
                                streamChannels=amtChannels)
            else:
                Constants.samplingRate = samplingRate
                pub.sendMessage("streamConnect", msg="CHANNELS_TOO_FEW", settingsChannels=Constants.numberOfChannels,
                                streamChannels=amtChannels)
        else:
            pub.sendMessage("streamConnect", msg="CONNECT_FAILED", settingsChannels=0, streamChannels=0)

    # Pulls samples from the LSL-stream, without saving them.
    # Needed for the times outside of the calibration and livesystem
    # -> buffer needs to be kept empty
    def keepPullingSamplesFromInlet(self):
        self.streamInlet.pull_sample()
        self.programMaster.setLastSampleTimestamp(pylsl.local_clock())
