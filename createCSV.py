import sortFunctions

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

def closeFiles(openedFiles, sourceCSV, comentsCSV):

    for file in openedFiles:
        file.close()
    sourceCSV.close()
    comentsCSV.close()

def readLine(file):

    line = file.readline()

    return line.rstrip() if line else chr(255)

def readFirstLines(openedFiles):
    
    lines = []
    for file in openedFiles:
        line = readLine(file)
        lines.append(line)
        
    return lines

def analyzeComment(comentsCSV, file, line, multiLineFlag=False):

    if multiLineFlag:
        if line.count("'''") == 2:
            if 'Autor' in line:
                comentsCSV.write(f',"{line[line.index("[") + 1:line.index("]")]}"')
            elif 'Ayuda' in line:
                comentsCSV.write(f',"{line[line.index("[") + 1:line.index("]")]}"')
            else:
                comentsCSV.write(f',"{line}"')
        elif line.count("'''") == 1:
            while not line.rstrip().endswith("'''"):
                if 'Autor' in line:
                    comentsCSV.write(f',"{line[line.index("[") + 1:line.index("]")]}"')
                elif 'Ayuda' in line:
                    comentsCSV.write(f',"{line[line.index("[") + 1:]}')
                else:
                    comentsCSV.write(f'{line.lstrip()}')
                line = readLine(file)
            comentsCSV.write('"')
    else:
        comentsCSV.write(f',"{line[line.index("#"):]}"')

    line = readLine(file)

    return line

def writeCSV(sourceCSV, comentsCSV, file, line, outOfFunctionLines):

    function = line[4:line.index('(')]
    parameters = line[line.index('('):line.index(')') + 1]
    if line[4:line.index(')') + 1] in outOfFunctionLines:
        sourceCSV.write(f'"*{function}","{parameters}"')
    else:
        sourceCSV.write(f'"{function}","{parameters}"')
    comentsCSV.write(f'"{function}"')

    line = readLine(file)
    while line != chr(255) and not line.startswith('def '):
        if line.lstrip().startswith("'''"):
            line = analyzeComment(comentsCSV, file, line, multiLineFlag=True)
        elif line.lstrip().startswith('#'):
            comentsCSV.write(f',"{line.rstrip()}"')
            line = readLine(file)
        elif '#' in line and not ('"#"' in line and '#todo' in line):
            line = analyzeComment(comentsCSV, file, line, multiLineFlag=False)
        else:   
            sourceCSV.write(f',"{line.rstrip()}"')
            line = readLine(file)

    sourceCSV.write('\n')
    comentsCSV.write('\n')
    
    return line

def merge(sourceCSV, comentsCSV, openedFiles, outOfFunctionLines):

    getMinLine = lambda x: min(x)

    firstLines = readFirstLines(openedFiles)
    minLine = getMinLine(firstLines)
    while minLine != chr(255):
        minLineIndex = firstLines.index(minLine)
        firstLines[minLineIndex] = writeCSV(sourceCSV, comentsCSV, openedFiles[minLineIndex], minLine, outOfFunctionLines)
        minLine = getMinLine(firstLines)

def createCSV():

    outOfFunctionLines, sortedCodesFileNames = sortFunctions.sortCodes('programas_ejemplo.txt')
    openedFiles = openSortedCodes(sortedCodesFileNames)
    sourceCSV = open('fuente_unico.csv', 'w')
    comentsCSV = open('comentarios.csv', 'w')

    merge(sourceCSV, comentsCSV, openedFiles, outOfFunctionLines)

    closeFiles(openedFiles, sourceCSV, comentsCSV)

createCSV()