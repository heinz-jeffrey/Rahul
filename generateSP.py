import rstr
from itertools import product
import sys
import os
import random
import math
import re
################################# HELPER FUNCTIONS ############################

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

def findPartition(n,length):
    x=0
    partitions = []
    t=length
    y=0
    while len(partitions) < n-1:
        if t!=0:
            y = random.randint(0,t)
            t=t-y
            x+=y
            partitions.append(y)
        if t==0:
            break
    if x!= length:
        if t!=0:
            partitions.append(length-x)
    if t==0:
        while len(partitions)<n:
            partitions.append(0)
    return partitions

############################### GENERATE SP FUNCTIONS #########################



def generateSPPositive(alphabet, sampleAmount, checkForbidden, minWordLength, maxWordLength):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = minWordLength
    while x < maxWordLength:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if not forbidden:
            samplePerLength.append(word)
            print(word, x, maxWordLength,len(samplePerLength), sampleAmount)        
        if len(samplePerLength) == sampleAmount:
            x += 1
            posSamples+=samplePerLength
            samplePerLength = []
    return posSamples

#optimization created for sp2 test2 only:

def generateSP2Positive(alphabet, sampleAmount, checkForbidden, minWordLength, maxWordLength):
    # GENERATE POSITIVE SAMPLES
    posSamples = []
    samplePerLength = []
    x = minWordLength
    alphabet1 = alphabet.replace('a','')
    alphabet2 = alphabet.replace('b','')
    while x < maxWordLength:
        partitions = []
        regex = '[alphabet1]{}[a][a]{}[alphabet2]{}'
        regex = regex.replace('alphabet1', alphabet1)
        regex = regex.replace('alphabet2', alphabet2)
        partitions += findPartition(3,x-1)
        for e in partitions:
            rep = "{"+str(e)+"}"
            regex=regex.replace("{}",rep,1)
        regex2 = '|[alphabet1]{x}'
        regex2 = regex2.replace('alphabet1',alphabet1)
        regex2 = regex2.replace('x',str(x))
        regex = regex+regex2
        word = rstr.xeger(regex)
        forbidden = checkForbidden(word)
        if not forbidden:
            samplePerLength.append(word)
            print(word, x, maxWordLength,len(samplePerLength), sampleAmount, regex)
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
    while len(samplePerLength)<(sampleAmount*minWordLength):
        word = rstr.rstr(alphabet,minWordLength)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
    x = minWordLength+1
    negSamples+=samplePerLength
    samplePerLength = []
    while x < maxWordLength:
        word = rstr.rstr(alphabet, x)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
            print(word, x, maxWordLength,len(samplePerLength), sampleAmount)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples


def generateSP4_8Negative(alphabet, minWordLength, maxWordLength, sampleAmount, checkForbidden, testOrTrain):
    # GENERATE POSITIVE SAMPLES
    negSamples = []
    samplePerLength = []
    regTemplate = ""
    if checkForbidden == checkForbiddenSP4:
        regTemplate = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
    if checkForbidden == checkForbiddenSP8:
        regTemplate = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
    regTemplate = regTemplate.replace('alphabet',alphabet)
    partitions=[]
    x = 0
    if testOrTrain == "train":
        while len(samplePerLength)<(sampleAmount*minWordLength):
            regMod=""
            if checkForbidden == checkForbiddenSP8:
                regMod =  '(abbaabba)'
            if checkForbidden == checkForbiddenSP4:
                regMod = '(abba)'
            word = rstr.xeger(regMod)
            # check if word is forbidden
            forbidden = checkForbidden(word)
            if forbidden:
                samplePerLength.append(word)
                print(word, len(word), testOrTrain)
        x = minWordLength+1
    else:
        x = minWordLength
    negSamples+=samplePerLength
    samplePerLength = []
    while x < maxWordLength:
        partitions = []
        if checkForbidden == checkForbiddenSP4:
            partitions += findPartition(5,x-4)
        if checkForbidden == checkForbiddenSP8:
            partitions += findPartition(9,x-8)
        regMod = regTemplate
        for e in partitions:
            rep = "{"+str(e)+"}"
            regMod=regMod.replace("{}",rep,1)
        word = rstr.xeger(regMod)
        # check if word is forbidden
        forbidden = checkForbidden(word)
        if forbidden:
            samplePerLength.append(word)
            print(word, len(word), testOrTrain)
        if len(samplePerLength) == sampleAmount:
            x += 1
            negSamples+=samplePerLength
            samplePerLength = []
    return negSamples



########################### WRITE TRAINING DATA ###############################

def writeTrainingData(trainDir,sp, alphabet):
    tSP = "./"+trainDir+"/Training_"+sp+"_positive.txt"
    f=open(tSP, "w")
    f.seek(0)

    tSP = "./"+trainDir+"/Training_"+sp+"_negative.txt"
    f1=open(tSP, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]

    if sp == "SP2":
        trainingPos = generateSPPositive(alphabet, 20, checkForbiddenSP2, 1, 26)
        trainingNeg = generateSPNegative(alphabet, 2, 26, 20, checkForbiddenSP2)
    elif sp =="SP4":
        trainingPos = generateSPPositive(alphabet, 200, checkForbiddenSP4, 1, 26)
        trainingNeg = generateSP4_8Negative(alphabet, 4, 26, 200, checkForbiddenSP4,"train")
    else:
        trainingPos = generateSPPositive(alphabet, 2000, checkForbiddenSP8, 1, 26)
        trainingNeg = generateSP4_8Negative(alphabet, 8, 26, 2000, checkForbiddenSP8,"train")

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')
    f.close()
    f1.close()
    return (trainingPos, trainingNeg)

##########################GENERATE TEST 1######################################
def generateSPTest1(alphabet,trainingSP, sampleAmount, posORneg, checkForbidden,m):
    samples=[]
    for t in range(1,m):
        print("--1--", posORneg, checkForbidden, m)
        if posORneg == 'POS':
            if allCombos[t] == None:
                allCombos[t] = [''.join(x) for x in product(alphabet, repeat = t)]
        print("--2--", posORneg, checkForbidden, m)
        if posORneg == 'POS':
            unknown = [k for k in allCombos[t] if k not in trainingSP]
        else:
            unknown = [k for k in negSamples if k not in trainingSP and len(k) == t]
        print("--3--", posORneg, checkForbidden, m)
        for x in unknown:
            if len(x) == t:
                if not forbiddenChecker(x, posORneg, checkForbidden):
                    samplePerLength = []
                    while len(samplePerLength)<sampleAmount:
                        word = random.choice(unknown)
                        forbidden = forbiddenChecker(word, posORneg, checkForbidden)
                        if not forbidden:
                            if word not in trainingSP:
                                samplePerLength.append(word)
                    samples+=samplePerLength
                    break
    for t in range(m, 26):
        samplePerLength = []
        while len(samplePerLength)<sampleAmount:
            word = rstr.rstr(alphabet, t)
            if (checkForbidden == checkForbiddenSP4) and (posORneg == 'NEG'):
                partitions = []
                regex = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
                regex = regex.replace("alphabet", alphabet)
                partitions += findPartition(5,t-4)
                for e in partitions:
                    rep = "{"+str(e)+"}"
                    regex=regex.replace("{}",rep,1)
                word = rstr.xeger(regex)
            if (checkForbidden == checkForbiddenSP8) and (posORneg == 'NEG'):
                partitions = []
                regex = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
                regex = regex.replace("alphabet", alphabet)
                partitions += findPartition(9,t-8)
                for e in partitions:
                    rep = "{"+str(e)+"}"
                    regex=regex.replace("{}",rep,1)
                word = rstr.xeger(regex)
            forbidden = forbiddenChecker(word, posORneg, checkForbidden)
            if not forbidden:
                if word not in trainingSP:
                    samplePerLength.append(word)
                    print(word, len(word), len(samplePerLength), sampleAmount, posORneg, "generateSPTest1",checkForbidden)
        samples+=samplePerLength

    #add extra samples
    extraSamples = []
    while len(extraSamples) < sampleAmount*10:
        word = rstr.rstr(alphabet, 25)
        # check if word is forbidden
        if (checkForbidden == checkForbiddenSP4) and (posORneg == 'NEG'):
            partitions = []
            regex = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
            regex = regex.replace("alphabet", alphabet)
            partitions += findPartition(5,25-4)
            for e in partitions:
                rep = "{"+str(e)+"}"
                regex=regex.replace("{}",rep,1)
            word = rstr.xeger(regex)
        if (checkForbidden == checkForbiddenSP8) and (posORneg == 'NEG'):
            partitions = []
            regex = '([alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{}a[alphabet]{}b[alphabet]{}b[alphabet]{}a[alphabet]{})'
            regex = regex.replace("alphabet", alphabet)
            partitions += findPartition(9,25-8)
            for e in partitions:
                rep = "{"+str(e)+"}"
                regex=regex.replace("{}",rep,1)
            word = rstr.xeger(regex)
        forbidden = forbiddenChecker(word, posORneg, checkForbidden)
        if not forbidden:
            if word not in trainingSP:
                extraSamples.append(word)
    samples+=extraSamples
    return samples

############################# WRITE TEST DATA ###############################


def writeTest1data(testDir,sp,alphabet):
    tSP = "./"+testDir+"/test1_"+sp+"_positive.txt"
    f1=open(tSP, "w")
    f1.seek(0)

    tSP = "./"+testDir+"/test1_"+sp+"_negative.txt"
    f2=open(tSP, "w")
    f2.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    negSamples = []
    m = 0
    if sp == "SP2":
        f=''
        if len(alphabet) == 3:
            f = open('./foma_outputs/sp2negative_3/sp2negative_3.txt','r')
            m=13
        if len(alphabet) == 10:
            f = open('./foma_outputs/sp2negative_10/sp2negative_10.txt','r')
            m=6
        if len(alphabet) == 56:
            f = open('./foma_outputs/sp2negative_56/sp2negative_56.txt','r')
            m=5
        for l in f:
            negSamples.append(l[:-1])            
        trainingPos = generateSPTest1(alphabet,trainingPosSP2, 20, 'POS', checkForbiddenSP2,m)
        trainingNeg = generateSPTest1(alphabet,trainingNegSP2, 20, 'NEG', checkForbiddenSP2,m)
    elif sp =="SP4":
        
        f=''
        if len(alphabet) == 3:
            f = open('./foma_outputs/sp4negative_3/sp4negative_3.txt','r')
            m=13
        if len(alphabet) == 10:
            f = open('./foma_outputs/sp4negative_10/sp4negative_10.txt','r')
            m=9
        if len(alphabet) == 56:
            f = open('./foma_outputs/sp4negative_56/sp4negative_56.txt','r')
            m=8
        for l in f:
            negSamples.append(l[:-1])
        if len(alphabet) > 3 :
            trainingPos = generateSPTest1(alphabet,trainingPosSP4, 200, 'POS', checkForbiddenSP4,5)
        else:
            trainingPos = generateSPTest1(alphabet,trainingPosSP4, 200, 'POS', checkForbiddenSP4,m)
        trainingNeg = generateSPTest1(alphabet,trainingNegSP4, 200, 'NEG', checkForbiddenSP4,m)
    else:

        f=''
        if len(alphabet) == 3:
            f = open('./foma_outputs/sp8negative_3/sp8negative_3.txt','r')
            m=11
        if len(alphabet) == 10:
            f = open('./foma_outputs/sp8negative_10/sp8negative_10.txt','r')
            m=9
        if len(alphabet) == 56:
            f = open('./foma_outputs/sp8negative_56/sp8negative_56.txt','r')
            m = 11
        for l in f:
            negSamples.append(l[:-1])

        if len(alphabet) > 3:
            x = 5
            if len(alphabet) > 10:
                x = 4
            trainingPos = generateSPTest1(alphabet,trainingPosSP8, 2000, 'POS', checkForbiddenSP8,x)
        else:
            trainingPos = generateSPTest1(alphabet,trainingPosSP8, 2000, 'POS', checkForbiddenSP8,m)
        trainingNeg = generateSPTest1(alphabet,trainingNegSP8, 2000, 'NEG', checkForbiddenSP8,m)

    for x in trainingPos:
        f1.write(x)
        f1.write('\n')
    for x in trainingNeg:
        f2.write(x)
        f2.write('\n')

    f.close()
    f1.close()
    f2.close()
    return (trainingPos, trainingNeg)


def writeTest2data(testDir,sp,alphabet):
    tSP = "./"+testDir+"/test2_"+sp+"_positive.txt"
    f=open(tSP, "w")
    f.seek(0) 

    tSP = "./"+testDir+"/test2_"+sp+"_negative.txt"
    f1=open(tSP, "w")
    f1.seek(0)
    
    trainingPos=[]
    trainingNeg=[]
    print("start test2 data")
    if sp == "SP2":
        print("start sp2 test2 data")
        trainingPos = generateSP2Positive(alphabet, 20, checkForbiddenSP2, 26, 51)
        trainingNeg = generateSPNegative(alphabet, 26, 51, 20, checkForbiddenSP2)
    elif sp =="SP4":
        print("start sp4 test2 data")
        trainingPos = generateSPPositive(alphabet, 200, checkForbiddenSP4, 26, 51)
        trainingNeg = generateSP4_8Negative(alphabet, 26, 51, 200, checkForbiddenSP4, "test")
    else:
        print("start sp8 test2 data")
        trainingPos = generateSPPositive(alphabet, 2000, checkForbiddenSP8, 26, 51)
        trainingNeg = generateSP4_8Negative(alphabet, 26, 51, 2000, checkForbiddenSP8, "test")

    for x in trainingPos:
        f.write(x)
        f.write('\n')
    for x in trainingNeg:
        f1.write(x)
        f1.write('\n')

    f.close()
    f1.close()
    return (trainingPos, trainingNeg)


##############################################################################
##############################################################################
if __name__ == "__main__":
    alphabet=sys.argv[1]
    trainDir=sys.argv[2]
    testDir=sys.argv[3]
    if not os.path.exists(trainDir):
        os.makedirs(trainDir)
    if not os.path.exists(testDir):
        os.makedirs(testDir)
############################################################################
######################### CREATE TRAINING SETS #############################
############################################################################
tset = writeTrainingData(trainDir,"SP2", alphabet)
trainingPosSP2 = tset[0]
trainingNegSP2 = tset[1]

tset = writeTrainingData(trainDir,"SP4", alphabet)
trainingPosSP4 = tset[0]
trainingNegSP4 = tset[1]

tset = writeTrainingData(trainDir,"SP8", alphabet)
trainingPosSP8 = tset[0]
trainingNegSP8 = tset[1]


############################################################################
######################### CREATE TEST SETS #################################
############################################################################

#########################   TEST 1  ######################################
allCombos = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

negSamples = []

test1setSP2 = writeTest1data(testDir,"SP2",alphabet)
test1PosSP2 = test1setSP2[0]
test1NegSP2 = test1setSP2[1]

test1setSP4 = writeTest1data(testDir,"SP4",alphabet)
test1PosSP4 = test1setSP4[0]
test1NegSP4 = test1setSP4[1]

test1setSP8 = writeTest1data(testDir,"SP8",alphabet)
test1PosSP8 = test1setSP8[0]
test1NegSP8 = test1setSP8[1]

#########################   TEST 2  ######################################

test2setSP2 = writeTest2data(testDir,"SP2", alphabet)
test2PosSP2 = test2setSP2[0]
test2NegSP2 = test2setSP2[1]

test2setSP4 = writeTest2data(testDir,"SP4", alphabet)
test2PosSP4 = test2setSP4[0]
test2NegSP4 = test2setSP4[1]

test2setSP8 = writeTest2data(testDir,"SP8", alphabet)
test2PosSP8 = test2setSP8[0]
test2NegSP8 = test2setSP8[1]
