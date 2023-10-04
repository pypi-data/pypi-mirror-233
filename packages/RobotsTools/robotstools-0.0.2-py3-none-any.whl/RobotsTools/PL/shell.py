import RobotsTools as rt

outputFile = f"{rt.dataLocation}/output.txt"
varFile = f"{rt.dataLocation}/var.ini"
rt.logFile(outputFile)
rt.setLogSettings(False)
rt.createConfigFile(varFile)

#
#      Function
#

class Function:
    def __init__(self, textSplit): 
        if textSplit[0] == "print":
            Function.fprint(textSplit)
        elif textSplit[0] == "add":
            Function.fadd(textSplit)
        elif textSplit[0] == "sub":
            Function.fsub(textSplit)
        elif textSplit[0] == "var":
            Function.fvar(textSplit)


    def fprint(textSplit):
        print(" ".join(textSplit[1:]))
        rt.log(" ".join(textSplit[1:]))


    def fadd(textSplit):
        if textSplit[2] == "and":
            print(eval(f"{int(textSplit[1])} + {int(textSplit[3])}"))
            rt.log(eval(f"{int(textSplit[1])} + {int(textSplit[3])}"))
        else:
            print("""missing the "and" after add""")


    def fsub(textSplit):
        if textSplit[2] == "and":
            print(eval(f"{int(textSplit[1])} - {int(textSplit[3])}"))
            rt.log(eval(f"{int(textSplit[1])} - {int(textSplit[3])}"))
        else:
            print("""missing the "and" after sub""")
        
    def fvar(textSplit):
        rt.addToConfigFile(varFile, " ".join(textSplit[1:]), textSplit[1])


###################################
#               RUN
###################################

def run(text, Line):
    Lexer(text, Line)

###################################
#               TokenTypes
###################################

keywords = ["input", "for", "print"]
#with open("keywords.txt", 'r') as keywordsfile:
#    keylines = keywordsfile.readlines()
#
#keyline = "".join(keylines)
#keywords = keyline.split("|")

operators = ["+", "-", "*", "/", "="]
varlist = ["int", "str", "bool"]

###################################
#               Operators
###################################

operatorsx = ["+", "-", "*", "/", "//", "**", "<", ">", "%", "=", "+=", "-=", "%=", "*=", "/=", "//=", "**/", "&=", "|=", "^=", ">>=", "<<=", "==", "!=", "<=", ">="]
parenthesis = ["(", ")"]

class Operators:
    def __init__(self, textTokens, textSplit, Line):
        pass

###################################
#               Lexer
###################################

class Lexer:
    def __init__(self, text, Line):
        self.text = text
        self.textSplit = text.split()

        Function(self.textSplit)
        rt.log(self.textSplit)


def runShell():
    Line = 0

    rt.truncateLogFile(outputFile)

    while True:
            text = input('shell > ')
            run(text, Line)
            Line = Line + 1