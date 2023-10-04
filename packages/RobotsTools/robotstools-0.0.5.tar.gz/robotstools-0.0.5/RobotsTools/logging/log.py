from ..config.getConfigValue import getConfigValue
from .formattedWrite import formattedWrite
from .debug import debug


import threading
lock = threading.Lock()

def log(message=str, LogMessageType=str(getConfigValue("defaultLogMessageType")), filename=str(getConfigValue("defaultLogFile"))):
    LogMessageType = LogMessageType.upper()
    if getConfigValue("LogSettings") == True:
        try:
            debug(str(message), LogMessageType)
            with lock:
                with open(filename, "a") as file:
                    file.write(formattedWrite(str(message), LogMessageType))
                    file.write("\n")
            return "log secceeded"
        except Exception as e:
            debug(f"!!! Could not log: {str(e)}, you might need to setLogSettings !!!")
            return e
    else:
        return "LogSettings is False"