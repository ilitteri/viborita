class Function:
    def __init__(self, sourceSplitedLine: str, commentSplittedLine: str):
        self.name = sourceSplitedLine[0][2:] if '*' in sourceSplitedLine[0] else sourceSplitedLine[0][1:]
        self.parameters = sourceSplitedLine[1]
        self.lines = sourceSplitedLine[3:]
        self.author = commentSplittedLine[1]
        self.help = commentSplittedLine[2]
        self.comments = commentSplittedLine[3:]
