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

def getTripleLineComment(file, line):
    comment = ''
    while not line.rstrip().endswith("'''"):
        comment += line.lstrip()
        line = readLine(file)
    comment += line.lstrip()
    print(comment)
    return comment

def analyzeMultiLineComment(comentsCSV, file, line, multiLineFlag=True):
    comment = getTripleLineComment(file, line)
    authorIndex = comment.find('Autor:')
    helpIndex = comment.find('Ayuda:')
    if authorIndex != -1:
        author = comment[authorIndex:comment.index(']')]
    else:
        author = 'Sin Autor'
    if helpIndex != -1:
        help = comment[helpIndex:comment.index(']', helpIndex)]
    else:
        help = ''
    
    return author, help

def writeCSV(sourceCSV, comentsCSV, file, line, outOfFunctionLines, fileName):

    function = line[4:line.index('(')]
    parameters = line[line.index('(') + 1:line.index(')')]
    if line[4:line.index(')') + 1] in outOfFunctionLines:
        sourceCSV.write(f'"*{function}","{parameters}","{fileName}"')
    else:
        sourceCSV.write(f'"{function}","{parameters}","{fileName}"')
    comentsCSV.write(f'"{function}"')

    line = readLine(file)
    while line != chr(255) and not line.startswith('def '):
        if line.lstrip().startswith("'''"):
            author, help = analyzeMultiLineComment(comentsCSV, file, line)
            comentsCSV.write(f',"{author}","{help}"')
        elif line.lstrip().startswith('#'):
            comentsCSV.write(f',"{line.rstrip()}"')
        elif '#' in line and not ('"#"' in line and '#todo' in line):
            sourceCSV.write(f',"{line[:line.index("#")]}"')
            comentsCSV.write(f',"{line[line.index("#"):]}"')
        else:   
            sourceCSV.write(f',"{line.rstrip()}"')
        line = readLine(file)

    sourceCSV.write('\n')
    comentsCSV.write('\n')
    
    return line

def merge(sourceCSV, comentsCSV, openedFiles, outOfFunctionLines, modules):

    getMinLine = lambda x: min(x)

    firstLines = readFirstLines(openedFiles)
    minLine = getMinLine(firstLines)
    while minLine != chr(255):
        minLineIndex = firstLines.index(minLine)
        firstLines[minLineIndex] = writeCSV(sourceCSV, comentsCSV, openedFiles[minLineIndex], minLine, outOfFunctionLines, modules[minLineIndex])
        minLine = getMinLine(firstLines)

def createCSV():

    outOfFunctionLines, sortedCodesFileNames, modules = sortFunctions.sortCodes('programas_ejemplo.txt')
    openedFiles = openSortedCodes(sortedCodesFileNames)
    sourceCSV = open('fuente_unico.csv', 'w')
    comentsCSV = open('comentarios.csv', 'w')

    merge(sourceCSV, comentsCSV, openedFiles, outOfFunctionLines, modules)

    closeFiles(openedFiles, sourceCSV, comentsCSV)

createCSV()