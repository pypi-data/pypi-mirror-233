import time
import threading
import os

#### genConfigFile
import configparser
dataLocation = "RobotsToolsData"
defaultConfigFile = f"{dataLocation}/RobotsToolsConfig.ini" # do not change unless you also change in main.py
defaultSection = 'default'


def genConfigFile():
    configFileGlobal = configparser.ConfigParser()
    configFileGlobal.add_section(defaultSection)
    
    configFileGlobal.set(defaultSection, "defaultLogFile", "logFile.txt")
    configFileGlobal.set(defaultSection, "defaultDataFile", "dataFile.txt")
    configFileGlobal.set(defaultSection, "defaultLogMessageType", "INFO")
    configFileGlobal.set(defaultSection, "defaultTimerLogMessageType", "TIMER")
    configFileGlobal.set(defaultSection, "defaultTimerMessage", "default timer")
    configFileGlobal.set(defaultSection, "DebugToggle", "True")
    configFileGlobal.set(defaultSection, "LogSettings", "True")
    configFileGlobal.set(defaultSection, "ClearLogFile", "True")
    configFileGlobal.set(defaultSection, "ClearDataFile", "True")

    print(configFileGlobal)
    with open(defaultConfigFile, "w") as configFile:
        configFile.write(configFileGlobal)

#def changeConfigFile(filename=str, id=str, content=str, type=str): # add logging # remove and change everything to just use the build in function in the file operations file
#    configFileGlobal = configparser.ConfigParser()
#    configFileGlobal.read(filename)
#
#    configFileGlobal.set(defaultSection, str(id), str(content))
#
#    with open(defaultConfigFile, "w") as configFile:
#        configFile.write(configFileGlobal)

def getConfigValue(request, section=defaultSection):
    # Create a ConfigParser object and read the config file
    try:
        configFileGlobal = configparser.ConfigParser()
        configFileGlobal.read(defaultConfigFile)

        value = configFileGlobal.get(section, request)
    except Exception as e:
        quit(f"!!! Could not load config file, error: {e} !!! {request}")

    return value
####

if os.path.exists(dataLocation):
    pass
else:
    os.mkdir(dataLocation)

if os.path.exists(defaultConfigFile):
    pass
else:
    genConfigFile()

#### addToConfigFile
def addToConfigFile(filename=str, id=[str, int], content=str, section=str("config")): # if trying to add a line that is the same a a line already in the file run an error instead of adding it anyway
    try:
        config = configparser.ConfigParser()
        config.read(filename)
        if config.has_section(section):
            pass
        else:
            config.add_section(section)

        config.set(section, str(id), str(content))
        with open(filename, "w") as configFile:
                configFile.write(config.write(configFile))
        log(f"Added '{str(content)}' to config file '{filename}'", "FILE EDIT")
        return
    except FileNotFoundError:
        log(f"!!! Could not add to config file '{filename}' it was not found!!!", "FILE ERROR")

    except Exception as e:
        log(f"!!! Could not add to config file '{filename}', error {e} !!!", "FILE ERROR")
#### addToConfigFile

#### setSettings
def setLogSettings(value=True):
    addToConfigFile(defaultConfigFile, "LogSettings", value, "default")

def setDebugToggle(value=True):
    addToConfigFile(defaultConfigFile, "DebugToggle", value, "default")

def setClearLogFile(value=True):
    addToConfigFile(defaultConfigFile, "ClearLogFile", value, "default")

def setClearDataFile(value=True):
    addToConfigFile(defaultConfigFile, "ClearDataFile", value, "default")

def changeDefaultLogFile(filename=str):
    addToConfigFile(defaultConfigFile, "defaultLogFile", filename, "default")
#### setSettings

#### main
try:
    with open(defaultConfigFile, 'r') as file:
        pass
except:
    genConfigFile()

lock = threading.Lock()

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
    
def truncateLogFile(filename=str):
    with open(filename, 'w') as file:
        file.truncate(0)

def LogList(message=str, LogMessageType=str(getConfigValue("defaultLogMessageType")), filename=str(getConfigValue("defaultLogFile"))):
    if getConfigValue("LogSettings") == True:
        try:
            for x in range(len(message)):
                debug(f"{str(message[x])} as index {str(x)} of list {[var for var in globals() if globals()[var] is message][0]}", LogMessageType)
                with open(filename, "a") as file:
                    file.write(formattedWrite(f"{str(message[x])} as index {str(x)} of list {[var for var in globals() if globals()[var] is message][0]}", LogMessageType))
                    file.write("\n")
            return
        except Exception as e:
            debug(f"!!! Could not log: {str(e)}, you might need to setLogSettings !!!", "ERROR")
    else:
        return
#### main

#### fileOperations
# in the config file make it for .ini files instead of how it is now
def loadFile(filename=str, mode=str("r")):
    with open(str(filename), mode) as file:
        fileContent = file.read().splitlines()
    log(f"Loaded file '{filename}' with content '{fileContent}'", "FILE LOAD")
    return fileContent

def saveFile(filename=str, content=str, mode=str("w")):
    with open(str(filename), mode) as file:
        file.write(content)
    log(f"Saved file '{filename}' with content '{content}'", "FILE WRITE")

# fix these with the new config file system

def writeToFile(filename=str, content=str, newline=bool(True), mode=str("a"),):
    try:
        with open(str(filename), mode) as file:
            file.write(str(content))
            if newline == True:
                file.write("\n")
        log(f"Wrote '{str(content)}' to file '{filename}'", "FILE WRITE")
    except FileNotFoundError:
        log(f"!!! Could not write to file '{filename}' it was not found!!!", "FILE ERROR")

    except:
        log(f"!!! Could not write to file '{filename}', unknown error!!!", "FILE ERROR")


def generateDataFile(data, filename=str(getConfigValue("defaultDataFile")), mode=str("a")):
    with open(filename, "w") as file:
        if getConfigValue("ClearDataFile") == True:
            file.truncate()
        else:
            pass
    if isinstance(data, list):
        with open(filename, mode) as file:
            for x in range(len(data)):
                file.write(f"{[var for var in globals() if globals()[var] is data][0]};{x}:{data[x]}\n")
    elif isinstance(data, str):
        with open(filename, mode) as file:
            file.write(f"{[var for var in globals() if globals()[var] is data][0]}:{data}")
    else:
        debug("!!!   invalid data type   !!!", "ERROR")

def createConfigFile(filename=str):
    if filename[-4:] == ".ini":
        pass
    if filename[-4:] == ".txt":
        quit("!!!   config file cannot be a .txt file (change it to .ini)   !!!")
    if "." not in filename:
        if filename[-3:] == "ini":
            quit("!!!   config file is missing a . (change it to .ini)   !!!")
        if filename[-3:] == "txt":
            quit("!!!   config file is missing a . and has txt instead of ini (change it to .ini)   !!!")
        filename = filename + ".ini"
        log("needed to add .ini to the end of the config file name (plz add it in the code)", "FILE WARNING")

    try:
        with open(str(filename), 'r') as file:
            pass
    except FileNotFoundError:
        try:
            config = configparser.ConfigParser()
            config.read(filename)
            section = "internal"
            config.add_section(section)
            
            config.set(section, "filename", filename)

            with open(filename, "w") as configFile:
                configFile.write(config.write(configFile))
                log(f"created config file {filename}", "FILE CREATED")
        except Exception as e:
            log(f"!!! Could not create config file '{filename}', error {e} !!!", "FILE ERROR")

def removeFromConfigFile(filename=str, id=[str, int]):
    pass

def getFromConfigFile(filename=str, id=[str, int] , section=str("config")):
    try:
        config = configparser.ConfigParser()
        config.read(filename)

        value = config.get(section, id)
    except Exception as e:
        quit(f"!!! Could not get from config file, error: {e} !!!")

    return value        
#### fileOperations

#### logFile
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
#### logFile

#### formattedWrite
def formattedWrite(message, LogMessageType=getConfigValue("defaultLogMessageType")):
    formattedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    outMessage = str(f"[{formattedTime}] [{LogMessageType}] {message}")
    return outMessage
#### formattedWrite

#### debug
def debug(message=str, LogMessageType=getConfigValue("defaultLogMessageType")):
    if getConfigValue("DebugToggle") == True:
        print(formattedWrite(message, LogMessageType))
#### debug

#### log
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
#### log

