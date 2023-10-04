from .formattedWrite import formattedWrite
from .getConfigValue import getConfigValue

def debug(message=str, LogMessageType=getConfigValue("defaultLogMessageType")):
    if getConfigValue("DebugToggle") == True:
        print(formattedWrite(message, LogMessageType))