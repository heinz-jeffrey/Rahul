import rstr
import re
from itertools import product


def forbiddenChecker(word, posORneg, checkForbidden):
    if posORneg == "POS":
        return checkForbidden(word)
    if posORneg == "NEG":
        return not checkForbidden(word)


#This Function checks if a word is forbidden in SP2

def checkForbiddenSP2(word):
    forbidden = False
    if re.search(".*".join("ab"), word):
        return True
    return False

#This Function checks if a word is forbidden in SP4

def checkForbiddenSP4(word):
    forbidden = False
    if re.search(".*".join("abba"), word):
        return True
    return False

#This Function checks if a word is forbidden in SP8

def checkForbiddenSP8(word):
    forbidden = False
    if re.search(".*".join("abbaabba"), word):
        return True
    return False

# GENERATE SP2 FOR APLHABET = {a,b,c}
def generateSPPositive(alphabet, sampleAmount, checkForbidden, minWordLength, maxWordLength):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = minWordLength
    while x < maxWordLength+1:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if not forbidden:
            samplePerLength.append(word)
            print(word,x)
        if len(samplePerLength) == sampleAmount:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

##########################################################################
########################NEGATIVE SAMPLES##################################
##########################################################################

def generateSPNegative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    while len(samplePerLength)<(20*minWordLength):
        word = rstr.rstr(alphabet,minWordLength)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
    x = minWordLength+1
    negSamples+=samplePerLength
    samplePerLength = []
    while x < maxWordLength+1:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples

def writeTrainingData(sp, alphabet):
    tSP = "./training/T_"+sp+".txt"
    f=open(tSP, "w")
    f.seek(0)
    trainingPos=[]
    trainingNeg=[]

    if sp == "SP2":
        trainingPos = generateSPPositive(alphabet, 20, checkForbiddenSP2, 1, 26)
        trainingNeg = generateSPNegative(alphabet, 2, 26, 20, checkForbiddenSP2)
    elif sp =="SP4":
        trainingPos = generateSPPositive(alphabet, 200, checkForbiddenSP4, 1, 26)
        trainingNeg = generateSPNegative(alphabet, 4, 26, 200, checkForbiddenSP4)
    else:
        trainingPos = generateSPPositive(alphabet, 2000, checkForbiddenSP8, 1, 26)
        trainingNeg = generateSPNegative(alphabet, 8, 26, 2000, checkForbiddenSP8)

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f.write(x)
        f.write('\n')
    f.close()
    return (trainingPos, trainingNeg)

##########################################################################
#########################CREATE TRAINING SETS#############################
##########################################################################

#tset = writeTrainingData("SP2", 'abc')
#trainingPosSP2 = tset[0]
#trainingNegSP2 = tset[1]

#tset = writeTrainingData("SP4", 'abc')
#trainingPosSP4 = tset[0]
#trainingNegSP4 = tset[1]

#tset = writeTrainingData("SP8", 'abc')
#trainingPosSP8 = tset[0]
#trainingNegSP8 = tset[1]


##########################################################################
#########################CREATE TEST SETS#################################
##########################################################################

#########################   TEST 1  ######################################

def generateSPTest1(alphabet,trainingSP, sampleAmount, posORneg, checkForbidden):
    samples=[]
    for t in range(1,26):
        allCombos = [''.join(x) for x in product(alphabet, repeat = t)]
        for x in allCombos:
            if len(x) == t:
                if x not in trainingSP:
                    if not forbiddenChecker(x, posORneg, checkForbidden):
                        samplePerLength = []
                        while len(samplePerLength)<sampleAmount:
                            word = rstr.rstr(alphabet, t)
                            # check if word is forbidden
                            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                            if not forbidden:
                                if word not in trainingSP:
                                    samplePerLength.append(word)
                            samples+=samplePerLength
        #add extra samples
        extraSamples = []
        while len(extraSamples) < sampleAmount*10:
            word = rstr.rstr(alphabet, 25)
            # check if word is forbidden
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSP:
                    extraSamples.append(word)
        samples+=extraSamples
        return samples

test1PosSP2 = generateSPTest1('abc',trainingPosSP2, 20, 'POS', checkForbiddenSP2)
test1PosSP4 = generateSPTest1('abc',trainingPosSP4, 200, 'POS', checkForbiddenSP4)
test1PosSP8 = generateSPTest1('abc',trainingPosSP8, 2000, 'POS', checkForbiddenSP8)

test1NegSP2 = generateSPTest1('abc',trainingNegSP2, 20, 'NEG', checkForbiddenSP2)
test1NegSP4 = generateSPTest1('abc',trainingNegSP4, 200, 'NEG', checkForbiddenSP4)
test1NegSP8 = generateSPTest1('abc',trainingNegSP8, 2000, 'NEG', checkForbiddenSP8)

#########################   TEST 2  ######################################
alphabet = 'abc'

test2PosSP2 = generateSPPositive(alphabet, 20, checkForbiddenSP2, 26, 50)
test2NegSP2 = generateSPNegative(alphabet, 26, 50, 20, checkForbiddenSP2)

test2PosSP4 = generateSPPositive(alphabet, 200, checkForbiddenSP4, 26, 50)
test2NegSP4 = generateSPNegative(alphabet, 26, 50, 200, checkForbiddenSP4)

test2PosSP8 = generateSPPositive(alphabet, 2000, checkForbiddenSP8, 26, 50)
test2NegSP8 = generateSPNegative(alphabet, 26, 50, 2000, checkForbiddenSP8)