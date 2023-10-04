from shell import *

with open("text.txt", 'r') as file:
    readlines = file.readlines()

with open("output.txt", 'w') as output:
    output.truncate(0)
    
for x in range(len(readlines)):
    try:
        readline = readlines[x].rstrip("\n")
    except:
        readline = readlines[x]

    Line = x
    run(readline, Line)