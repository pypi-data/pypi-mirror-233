defaultLogFile = "logfile.txt"

def change_logfile(new_filename):
    global defaultLogFile
    defaultLogFile = new_filename

print(defaultLogFile)
change_logfile("newlogfile.txt")
print(defaultLogFile)