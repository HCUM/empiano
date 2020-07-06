import datetime
from storage import constants

def timestampToCsv(timestamp):
    csv = open("./csv/TimeCorrection.csv", "a")
    csv.write(str(timestamp)+"\n")

def markerToCsv(marker):
    now = datetime.datetime.now()
    csv = open("./csv/" + now.strftime("%Y-%m-%d_%H.%M.%S_") + "Marker.csv", "w")
    #columnTitleRow = "modon, modoff\n"
    #csv.write(columnTitleRow)
    for (modon, modoff) in marker:
        row = str(modon) + "," + str(modoff) + "\n"
        csv.write(row)

def timestampMarkerToCsv(timestampMarker, origin):
    now = datetime.datetime.now()
    csv = open(constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_") + origin+ "TimestampMarker.csv", "w")

    for (modon, modoff) in timestampMarker:
        row = str(modon) + "," + str(modoff) + "\n"
        csv.write(row)

def dataPlusTimestampsToCsv(data, origin):
    now = datetime.datetime.now()
    csv = open(constants.savePath+ now.strftime("%Y-%m-%d_%H.%M.%S_") + origin +"DataTimestamps.csv", "w")
    columnTitleRow = "Channel1,Channel2,Channel3,Channel4,Channel5,Channel6,Channel7,Channel8,x,y,z,smth,Timestamp\n"
    csv.write(columnTitleRow)
    for (array, timestamp) in data:
        row = ""
        for value in array:
            row += str(value) + ","
        row += str(timestamp) + "\n"
        csv.write(row)


def wholeDataToCsv(data):
    now = datetime.datetime.now()
    csv = open("./csv/"+ now.strftime("%Y-%m-%d_%H.%M.%S_") +"WholeData.csv", "w")
    for channel in data:
        row = ""
        for value in channel:
            row += str(value) + ","
        row += "\n"
        csv.write(row)

def featuresToCsv(name, features):
    now = datetime.datetime.now()
    csv = open(constants.savePath+ now.strftime("%Y-%m-%d_%H.%M.%S_") +name+"Feature.csv", "w")
    columnTitleRow = "rms1, rms2, rms3, rms4, rms5, rms6, rms7, rms8, " \
                     "rms1/rms2, rms1/rms3, rms1/rms4, rms1/rms5, rms1/rms6, rms1/rms7, rms1/rms8," \
                     "rms2/rms3, rms2/rms4, rms2/rms5, rms2/rms6, rms2/rms7, rms2/rms8," \
                     "rms3/rms4, rms3/rms5, rms3/rms6, rms3/rms7, rms3/rms8," \
                     "rms4/rms5, rms4/rms6, rms4/rms7, rms4/rms8," \
                     "rms5/rms6, rms5/rms7, rms5/rms8," \
                     "rms6/rms7, rms6/rms8," \
                     "rms7/rms8\n"

    csv.write(columnTitleRow)
    for feature in features:
        row = ""
        for value in feature:
            row += str(value)+","
        row += "\n"
        csv.write(row)

def featureClassesToCsv(name, featureClasses):
    now = datetime.datetime.now()
    csv = open(constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_") + name + "FeatureClasses.csv", "w")
    for feature in featureClasses:
        csv.write(feature+"\n")


def dataToCsv(augData, nonAugData):
    now = datetime.datetime.now()
    augNames = ["normalMod", "slowMod", "fastMod", "mixedMod"]
    names = ["lightPlay", "noPlay", "fastPlay", "normalPlay"]
    for data, name in zip(augData, augNames):
        csv = open("./csv/" +now.strftime("%Y-%m-%d_%H.%M.%S_")+ name + "Data.csv", "w")
        columnTitleRow = "Channel 1, Channel 2, Channel 3, Channel 4, Channel 5, Channel 6, Channel 7, Channel 8\n"
        csv.write(columnTitleRow)
        for some in zip(data[0], data[1], data[2], data[3]):#, data[4], data[5], data[6], data[7]):
            row = ""
            for value in some:
                row += str(value) + ","
            row += "\n"
            csv.write(row)

    for data, name in zip(nonAugData, names):
        csv = open("./csv/" +now.strftime("%Y-%m-%d_%H.%M.%S_")+ name + "Data.csv", "w")
        columnTitleRow = "Channel 1, Channel 2, Channel 3, Channel 4, Channel 5, Channel 6, Channel 7, Channel 8\n"
        csv.write(columnTitleRow)
        for some in zip(data[0], data[1], data[2], data[3]):#, data[4], data[5], data[6], data[7]):
            row = ""
            for value in some:
                row += str(value) + ","
            row += "\n"
            csv.write(row)