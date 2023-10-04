from .main import *

def startTimer(message=str(getConfigValue("defaultTimerMessage")), LogMessageType=str(getConfigValue("defaultTimerLogMessageType")), filename=str(getConfigValue("defaultLogFile"))):
    global startTime
    startTime = time.time()
    formattedStartTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime))
    log(f"Timer '{message}' Started {formattedStartTime}", LogMessageType, filename)

def stopTimer(message=str(getConfigValue("defaultTimerMessage")), LogMessageType=str(getConfigValue("defaultTimerLogMessageType")), filename=str(getConfigValue("defaultLogFile"))):
    global endTime
    endTime = time.time()
    formattedEndTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime))
    timeTaken = endTime - startTime
    log(f"Timer '{message}' Stopped {formattedEndTime} total time taken (in seconds) {timeTaken}", LogMessageType, filename)
