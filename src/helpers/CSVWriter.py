import datetime
from storage import Constants

def timestampToCsv(timestamp):
    csv = open("./csv/TimeCorrection.csv", "a")
    csv.write(str(timestamp)+"\n")


def timestampMarkerToCsv(timestampMarker, origin):
    now = datetime.datetime.now()
    csv = open(Constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_") + origin + "TimestampMarker.csv", "w")

    for (modon, modoff) in timestampMarker:
        row = str(modon) + "," + str(modoff) + "\n"
        csv.write(row)


def dataPlusTimestampsToCsv(data, origin):
    now = datetime.datetime.now()
    csv = open(Constants.savePath + now.strftime("%Y-%m-%d_%H.%M.%S_") + origin + "DataTimestamps.csv", "w")
    columnTitleRow = "Channel1,Channel2,Channel3,Channel4,Channel5,Channel6,Channel7,Channel8,x,y,z,smth,Timestamp\n"
    csv.write(columnTitleRow)
    for (array, timestamp) in data:
        row = ""
        for value in array:
            row += str(value) + ","
        row += str(timestamp) + "\n"
        csv.write(row)
