import sortFunctions
import os

def openSortedCodes(fileNames):

    openedFiles = []
    for fileName in fileNames:
        openedFiles.append(open(fileName, 'r'))

    return openedFiles

def closeFiles(openedFiles, sourceCSV, commentsCSV):

    for file in openedFiles:
        file.close()
    sourceCSV.close()
    commentsCSV.close()

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

    return comment

def analyzeMultiLineComment(commentsCSV, file, line, multiLineFlag=True):

    comment = getTripleLineComment(file, line)
    authorIndex = comment.find('Autor:')
    helpIndex = comment.find('Ayuda:')

    if authorIndex != -1:
        author = comment[authorIndex:comment.index(']')]
    else:
        author = ''
    if helpIndex != -1:
        help = comment[helpIndex:comment.index(']', helpIndex)]
    else:
        help = ''
    if authorIndex == helpIndex == -1:
        otherComment = comment
    else:
        otherComment = ''
    
    return author, help, otherComment

def clasifyLine(sourceCSV, commentsCSV, file, line, multiLineFlag):
    
    if line.lstrip().startswith("'''"):
        multiLineFlag = True
        author, help, otherComment = analyzeMultiLineComment(commentsCSV, file, line)
        commentsCSV.write(f',"{author}","{help}","{otherComment}"')
    elif not multiLineFlag:
        multiLineFlag = True
        commentsCSV.write(',"",""')
    elif line.lstrip().startswith('#'):
        commentsCSV.write(f',"{line.rstrip()}"')
    elif '#' in line and not ('"#"' in line and '#todo' in line):
        sourceCSV.write(f',"{line[:line.index("#")]}"')
        commentsCSV.write(f',"{line[line.index("#"):]}"')
    else:   
        sourceCSV.write(f',"{line.rstrip()}"')

    return multiLineFlag

def writeCSV(sourceCSV, commentsCSV, file, line, outOfFunctionLines, fileName):

    multiLineFlag=False

    function = line[4:line.index('(')]
    parameters = line[line.index('(') + 1:line.index(')')]
    if line[4:line.index(')') + 1] in outOfFunctionLines:
        sourceCSV.write(f'"*{function}","{parameters}","{fileName}"')
    else:
        sourceCSV.write(f'"{function}","{parameters}","{fileName}"')
    commentsCSV.write(f'"{function}"')

    line = readLine(file)
    while line != chr(255) and not line.startswith('def '):
        multiLineFlag = clasifyLine(sourceCSV, commentsCSV, file, line, multiLineFlag)
        line = readLine(file)

    sourceCSV.write('\n')
    commentsCSV.write('\n')
    
    return line

def merge(sourceCSV, commentsCSV, openedFiles, outOfFunctionLines, modules):

    getMinLine = lambda x: min(x)

    firstLines = readFirstLines(openedFiles)
    minLine = getMinLine(firstLines)
    while minLine != chr(255):
        minLineIndex = firstLines.index(minLine)
        firstLines[minLineIndex] = writeCSV(sourceCSV, commentsCSV, openedFiles[minLineIndex], minLine, outOfFunctionLines, modules[minLineIndex])
        minLine = getMinLine(firstLines)

def deleteFiles(sortedCodesFilePaths):
    for path in sortedCodesFilePaths:
        os.remove(path)

def createCSV():

    outOfFunctionLines, sortedCodesFileNames, modules = sortFunctions.sortCodes('programas.txt')
    openedFiles = openSortedCodes(sortedCodesFileNames)
    sourceCSV = open('fuente_unico.csv', 'w')
    commentsCSV = open('comentarios.csv', 'w')

    merge(sourceCSV, commentsCSV, openedFiles, outOfFunctionLines, modules)

    closeFiles(openedFiles, sourceCSV, commentsCSV)

    sortedCodesFilePaths = [os.path.abspath(fileName) for fileName in sortedCodesFileNames]
    deleteFiles(sortedCodesFilePaths)

createCSV()