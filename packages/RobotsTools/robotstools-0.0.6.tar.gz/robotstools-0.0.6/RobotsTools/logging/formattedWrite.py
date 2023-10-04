import time
from .getConfigValue import getConfigValue

def formattedWrite(message, LogMessageType=getConfigValue("defaultLogMessageType")):
    formattedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    outMessage = str(f"[{formattedTime}] [{LogMessageType}] {message}")
    return outMessage