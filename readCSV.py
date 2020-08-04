class Function:
    def __init__(self, sourceSplitedLine: str, commentSplittedLine: str):
        self.name = sourceSplitedLine[0][2:] if '*' in sourceSplitedLine[0] else sourceSplitedLine[0][1:]
        self.parameters = sourceSplitedLine[1].split(',')
        self.lines = sourceSplitedLine[3:]
        self.author = commentSplittedLine[1]
        self.help = commentSplittedLine[2]
        self.comments = commentSplittedLine[3:]
        self.linesCount = len(self.lines)
        self.parametersCount = len(self.parameters)
        self.commentsCount = len(self.comments)
        self.statements = Statements(self.lines)

class Statements:
    def __init__(self, lines: list):
        self.forCounter = 0
        self.returnCounter = 0
        self.ifElifCounter = 0
        self.whileCounter = 0
        self.breakCounter = 0
        self.exitCounter = 0

        for line in self.lines:
            if "for " in line:
                self.forCounter += line.count("for")
            if "return " in line:
                self.returnCounter += 1
            if "if " in line: 
                self.ifElifCounter += 1
            if "while " in line:
                self.whileCounter += 1
            if "break" in line:
                self.breakCounter += 1
            if "exit" in line:
                self.exitCounter += 1

def getFunctions():
    functions = []
    with open('fuente_unico.csv', 'r') as sourceCSV, open('comentarios.csv', 'r') as commentsCSV:
        sourceLine = sourceCSV.readline().rstrip('\n')
        commentsLine = commentsCSV.readline().rstrip('\n')
        while sourceLine and commentsLine:
            functions.append(Function(sourceLine.split('","'), commentsLine.split('","')))
            sourceLine = sourceCSV.readline().rstrip('\n')
            commentsLine = commentsCSV.readline().rstrip('\n')