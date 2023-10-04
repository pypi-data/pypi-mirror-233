import os
from ..config.getConfigValue import getConfigValue

def logFile(filename=str, ClearLogFile=bool(getConfigValue("ClearLogFile"))):
    changeDefaultLogFile(filename)
    if os.path.exists(filename):
        if ClearLogFile == True:
            with open(filename, 'w') as file:
                file.truncate(0)
            return "File exists truncated"
        else:
            return "File exists not truncated"
    else:
        with open(filename, 'w') as file:
            pass
        return "File created"