from livesystem.ProgramMaster import main
from storage import Constants
import logging
import datetime
import sys

def initLogger():
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    now = datetime.datetime.now()
    #TODO ADJUSTED for study!!
    pathFile = Constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S") + '.log'
    fh = logging.FileHandler(pathFile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logging.getLogger().addHandler(sh)
    logging.getLogger().addHandler(fh)
    logAllConstants(logger)

def logAllConstants(logger):
    logger.info("MAIN: Current Constants:")
    logger.info("Sampling-Rate: %f", Constants.samplingRate)
    logger.info("lower bound of the cut out frequency: %f", Constants.lowerBoundCutOutFreq)
    logger.info("upper bound of the cut out frequency: %f", Constants.upperBoundCutOutFreq)
    logger.info("low band-stop frequency: %f", Constants.lowBandStopFreq)
    logger.info("high band-stop frequency: %f", Constants.highBandStopFreq)
    logger.info("Amount of channels: %d", Constants.numberOfChannels)
    logger.info("Window-size: %f", Constants.windowSize)
    logger.info("Samples per window: %d", Constants.samplesPerWindow)
    logger.info("Samples of a window shift: %d", Constants.windowShift)
    logger.info("Effect: %s", Constants.effect)
    logger.info("Recording file: %s", Constants.fileNameOfRecording)
    logger.info("lowest valid channel: %d", Constants.lowestValidChannel)
    logger.info("highest valid channel: %d", Constants.highestValidChannel)
    logger.info("calibration order: %s", Constants.calibrationOrder)
    logger.info("secondsOfCaliTasks: %d", Constants.secondsOfCaliTasks)
    logger.info("secondsOfCaliPause: %d", Constants.secondsOfCaliPause)
    logger.info("amt of samples to cut out: %d", Constants.amtSamplesToCutOff)


if __name__ == '__main__':
    initLogger()
    main()
