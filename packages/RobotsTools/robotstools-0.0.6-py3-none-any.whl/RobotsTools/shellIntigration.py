import os
import subprocess

def runShellCommand(command=str):
    os.system(command)

def runShellFile(filename=str):
    subprocess.call(['sh', f"./{filename}"])
