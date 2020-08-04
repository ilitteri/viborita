class Function:
    def __init__(self, sourceSplitedLine: str, commentSplittedLine: str):
        self.name = sourceSplitedLine[0][2:] if '*' in sourceSplitedLine[0] else sourceSplitedLine[0][1:]
        self.parameters = sourceSplitedLine[1].split(',')
        self.module = sourceSplitedLine[2]
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
        self.forCount = 0
        self.returnCount = 0
        self.ifElifCount = 0
        self.whileCount = 0
        self.breakCount = 0
        self.exitCount = 0

        for line in self.lines:
            if "for " in line:
                self.forCount += line.count("for")
            if "return " in line:
                self.returnCount += 1
            if "if " in line: 
                self.ifElifCount += 1
            if "while " in line:
                self.whileCount += 1
            if "break" in line:
                self.breakCount += 1
            if "exit" in line:
                self.exitCount += 1

def getFunctions():
    functions = []
    with open('fuente_unico.csv', 'r') as sourceCSV, open('comentarios.csv', 'r') as commentsCSV:
        sourceLine = sourceCSV.readline().rstrip('\n')
        commentsLine = commentsCSV.readline().rstrip('\n')
        while sourceLine and commentsLine:
            functions.append(Function(sourceLine.split('","'), commentsLine.split('","')))
            sourceLine = sourceCSV.readline().rstrip('\n')
            commentsLine = commentsCSV.readline().rstrip('\n')