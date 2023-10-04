from ..data import defaultConfigFile, defaultSection
import configparser

def getConfigValue(request, section=defaultSection):
    # Create a ConfigParser object and read the config file
    try:
        configFileGlobal = configparser.ConfigParser()
        configFileGlobal.read(defaultConfigFile)

        value = configFileGlobal.get(section, request)
    except Exception as e:
        quit(f"!!! Could not load config file, error: {e} !!! {request}")

    return value