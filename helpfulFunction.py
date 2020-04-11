import datetime

def getDateTimeStamp():
    return datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))