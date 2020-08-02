import os

def getPaths(file_name):
    with open(file_name, 'r') as file:
        return [(path, os.path.basename(path)) for path in [line.strip() for line in file.readlines()]]

class Function:
    def __init__(self, lines: list):
        self.name = lines[0][4:lines[0].index('(')]
        self.parameters = lines[0][lines[0].index('(') + 1:lines[0].index(')')].split(',')
        self.lines = lines[1:]

    def __repr__(self):
        parametersString = ', '.join(self.parameters)
        definition = f'def {self.name}({parametersString}):'
        return '\n'.join([definition] + self.lines) + '\n'

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

def readCode(code, mainFunctionFlag = False):
    functions = []
    outOfFunctionLines = []
    flag = False
    line = code.readline()
    while line:
        strippedLine = line.rstrip('\n')
        if line.startswith('def'):
            if flag:
                functions.append(Function(function))
            function = []
            function.append(strippedLine.replace('"', "'"))
            flag = True
        if flag and line.startswith('    '):
            function.append(strippedLine.replace('"', "'"))
        else:
            if strippedLine and mainFunctionFlag:
                outOfFunctionLines.append(strippedLine)
        line = code.readline()
    functions.append(Function(function))

    return functions, outOfFunctionLines

def writeSortedCodes(sortedCode, functions):
    for function in sorted(functions):
        sortedCode.write(repr(function))

def sortCodes(pathsContainer):
    sortedCodesFileNames = []
    pathsData = getPaths(pathsContainer)
    for path, fileName in pathsData:
        sortedCodeFileName = f'sorted_{fileName}'
        sortedCodesFileNames.append(sortedCodeFileName)
        with open(path, 'r') as code, open(f'{sortedCodeFileName}', 'w') as sortedCode:
            if path == pathsData[0][0]:
                functions, outOfFunctionLines = readCode(code, mainFunctionFlag=True)
                writeSortedCodes(sortedCode, functions)
            else:
                functions, outOfFunctionLines = readCode(code, mainFunctionFlag=False)
                writeSortedCodes(sortedCode, functions)
    
    return outOfFunctionLines, sortedCodesFileNames

#######################################################
'''def getSortedCodesPaths():    
    files = os.listdir('functions/')
    if 'desktop.ini' in files:
        files.remove('desktop.ini')

    return files'''

def openSortedCodes(fileNames):
    openedFiles = []
    for fileName in fileNames:
        openedFiles.append(open(fileName, 'r'))

    return openedFiles

def closeSortedCodes(openedFiles):
    for file in openedFiles:
        file.close()

def readLine(file):
    line = file.readline()
    return line.rstrip() if line else chr(255)

def readFirstLines(openedFiles):
    lines = []
    for file in openedFiles:
        line = readLine(file)
        lines.append(line)
        
    return lines

outOfFunctionLines, sortedCodesFileNames = sortCodes('programas_ejemplo.txt')
openedFiles = openSortedCodes(sortedCodesFileNames)
closeSortedCodes(openedFiles)






