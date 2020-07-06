from livesystem.liveSysManager import main
from storage import constants
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
    pathFile = constants.savePath+ now.strftime("%Y-%m-%d_%H.%M.%S")+'.log'
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
    logger.info("Sampling-Rate: %f", constants.samplingRate)
    logger.info("lower bound of the cut out frequency: %f", constants.lowerBoundCutOutFreq)
    logger.info("upper bound of the cut out frequency: %f", constants.upperBoundCutOutFreq)
    logger.info("low band-stop frequency: %f", constants.lowBandStopFreq)
    logger.info("high band-stop frequency: %f", constants.highBandStopFreq)
    logger.info("Amount of channels: %d", constants.numberOfChannels)
    logger.info("Window-size: %f", constants.windowSize)
    logger.info("Samples per window: %d", constants.samplesPerWindow)
    logger.info("Samples of a window shift: %d", constants.windowShift)
    logger.info("Effect: %s", constants.effect)
    logger.info("Recording file: %s", constants.fileNameOfRecording)
    logger.info("lowest valid channel: %d", constants.lowestValidChannel)
    logger.info("highest valid channel: %d", constants.highestValidChannel)
    logger.info("calibration order: %s", constants.calibrationOrder)
    logger.info("secondsOfCaliTasks: %d", constants.secondsOfCaliTasks)
    logger.info("secondsOfCaliPause: %d", constants.secondsOfCaliPause)
    logger.info("amt of samples to cut out: %d", constants.amtSamplesToCutOff)


if __name__ == '__main__':
    initLogger()
    main()
