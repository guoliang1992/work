#!/usr/bin/env python
#coding=gbk

import numpy as np
import pandas as pd
import jieba
from handler_character import HandlerStr as handler_str

def loadDataSet2():
	neg=pd.read_excel('data/test_neg.xls', header=None, index = None)
	pos=pd.read_excel('data/test_pos.xls', header=None, index = None)
	combined = np.concatenate((pos[0],neg[0]))
	y = np.concatenate((np.ones(len(pos),dtype=int),np.zeros(len(neg),dtype=int)))
	text_lst = []
	
	for document in combined:
		document = handler_str().remove_special_character(document)
		document = document.replace('\n', '')
		text_lst.append(jieba.lcut(document))

	return text_lst, y

def createVocabList(dataSet):
	vocabSet = set([]) #创建一个set集合
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

def setOfWord2Vec(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary!" % word
	
	return returnVec

def bagOfWord2VecMN(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
		else:
			print "the word: %s is not in my Vocabulary!" % word
	
	return returnVec

def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	p0Num = np.ones(numWords);p1Num = np.ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = np.log(p1Num/p1Denom)
	p0Vect = np.log(p0Num/p0Denom)
	return p0Vect,p1Vect,pAbusive

def trainNb1(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	p0Num = np.ones(numWords);p1Num = np.ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	return p1Num, p0Num

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	p1 = sum(vec2Classify * p1Vec) + np.log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + np.log(1 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts, listClasses = loadDataSet2()
	myVocabList = createVocabList(listOPosts)
	trainMat=[]
	num = 0
	for postinDoc in listOPosts:
		trainMat.append(setOfWord2Vec(myVocabList, postinDoc))

	p0v, p1v = trainNb1(np.array(trainMat), np.array(listClasses))
	for i in xrange(len(myVocabList)):
		print "%s\t%s\t%s" % (myVocabList[i].encode('gbk'), str(int(p0v[i])),str(int(p1v[i])))
	
	#p0V, p1V, pAb = trainNB0(np.array(trainMat), np.array(listClasses))
	#np.savetxt('posArrData', p0V)
	#np.savetxt('negArrData', p1V)
	#np.savetxt('pabData')

	#p0V = np.loadtxt('posArrData')
	#p1V = np.loadtxt('negArrData')
	#pAb = 0.5
	#count = 0
	#for line in open('data/test_data.txt'):
	#	line = line.rstrip('\n')
	#	data, cla = line.split('\t')
	#	document = handler_str().remove_special_character(data.decode('gbk', 'ignore'))
	#	testEntry = jieba.lcut(document)

	#	thisDoc = np.array(setOfWord2Vec(myVocabList, testEntry))
	#	relCla =  classifyNB(thisDoc, p0V, p1V, pAb)
	#	print 'relCla:%d\tcla:%s' % (relCla, cla)

	#	if int(cla) == int(relCla):
	#		count += 1
	#print count

def textParse(bigString):
	import re
	listOfTokens = re.split(r'\W*', bigString)
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def textParse2(string):
	import jieba
	return jieba.cut(string)

def spamTest():
	docList = []; classList = []; fullText = []
	for i in range(1, 26):
		wordList = textParse(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)

		wordList = textParse(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	
	vocatList = createVocabList(docList)
	
	trainingSet = range(50); testSet = []
	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	
	trainMat = []; trainClasses = []
	for docIndex in trainingSet:
		trainMat.append(bagOfWord2VecMN(vocatList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V, p1V, pSpam = trainNB0(np.array(trainMat), np.array(trainClasses))

	errorCount = 0
	for docIndex in testSet:
		wordVector = bagOfWord2VecMN(vocatList, docList[docIndex])
		if classifyNB(np.array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
			print "classification error",docList[docIndex]
	print 'the error rate is: ',float(errorCount)/len(testSet)


 
#listOPosts, listClasses = loadDataSet()
#myVocabList = createVocabList(listOPosts)
#print myVocabList
#trainMat=[]
#for postinDoc in listOPosts:
#	trainMat.append(setOfWord2Vec(myVocabList, postinDoc))
#p0V,plV,pAb=trainNB0(trainMat, listClasses)

#str = "天街小雨润如酥，草色遥看近却无。最是一年春好处，绝胜烟柳满皇都"
#for word in textParse2(str):
#	print word

testingNB()
