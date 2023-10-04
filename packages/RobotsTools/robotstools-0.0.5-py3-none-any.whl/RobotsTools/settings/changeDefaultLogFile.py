

def changeDefaultLogFile(filename=str):
    addToConfigFile(defaultConfigFile, "defaultLogFile", filename, "default")