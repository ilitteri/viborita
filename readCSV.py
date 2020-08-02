class Function:
    def __init__(self, sourceSplitedLine: str, commentSplittedLine: str):
        self.name = sourceSplitedLine[0][2:] if '*' in sourceSplitedLine[0] else sourceSplitedLine[0][1:]
        self.parameters = sourceSplitedLine[1][1:-1]
        self.lines = sourceSplitedLine[3:]
        self.author = commentSplittedLine[1]
        self.help = commentSplittedLine[2]
        self.comments = commentSplittedLine[3:]

functions = []

with open('fuente_unico.csv', 'r') as sourceCSV, open('comentarios.csv', 'r') as commentsCSV:
    sourceLine = sourceCSV.readline().rstrip('\n')
    commentsLine = commentsCSV.readline().rstrip('\n')
    while sourceLine and commentsLine:
        functions.append(Function(sourceLine.split('","'), commentsLine.split('","')))
        sourceLine = sourceCSV.readline().rstrip('\n')
        commentsLine = commentsCSV.readline().rstrip('\n')