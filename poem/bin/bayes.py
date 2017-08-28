#!/usr/bin/env python
#coding=gbk

from numpy import *
import numpy as np
def createVocabList(dataSet):
	vocabSet = set([]) #创建一个set集合
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

def bagOfWord2VecMN(vocabList, inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
		else:
			print "the word: %s is not in my Vocabulary!" % word
	return returnVec


#接受两个参数 其中一个是全部的值切词之后的向量，另一个是class
def trainNB1(trainMatrix, trainCategory, CategoryNum):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pNbusive = {}
	for i in trainCategory:
		key = "p" + str(i) + "busive"
		if key not in pNbusive:
			pNbusive[key] = 1
		else:
			pNbusive[key] += 1
	
	for key in pNbusive:
		pNbusive[key] = pNbusive[key] / float(numTrainDocs)
	
	pNNum = {}
	pNDenom = {}
	for i in range(CategoryNum):
		key= "p" + str(i) + "Num"
		pNNum[key] = ones(numWords)
		key2 = "p" + str(i) + "Denom"
		pNDenom[key2] = 2.0
	
	for i in range(numTrainDocs):
		case = trainCategory[i]
		key = "p" + str(case) + "Num"
		key2 = "p" + str(case) + "Denom"
		pNNum[key] += trainMatrix[i]
		pNDenom[key2] += sum(trainMatrix[i])
		
	pNVect = {}
	for i in range(CategoryNum):
		key= "p" + str(i) + "Num"
		key2 = "p" + str(i) + "Denom"
		key3 = "p" + str(i) + "Vect"
		pNVect[key3] = log(pNNum[key] / pNDenom[key2])

	return pNVect, pNbusive

def classifyNB2(vec2Classify, pNVect, pNbusive, num):
	pN = {}
	for i in range(num):
		key = "p" + str(i) + "Vect"
		key2 = "p" + str(i) + "busive"
		key3= "p" + str(i)
		pN[key3] = sum(vec2Classify * pNVect[key] + log(pNbusive[key2]))
	return sorted(pN.iteritems(), key=lambda d:d[1], reverse=True)

def textParse2(string):
	import jieba
	return jieba.lcut(string)
	
class_flag = {}
num = 0
for line in open("conf/category"):
	line = line.rstrip("\n")
	if line in class_flag:
		continue
	else:
		class_flag[line] = num
		num += 1

shi_type = {}
for line in open('conf/type_category'):
	line = line.rstrip("\n")
	segs = line.split("\t")
	shi_type[segs[1]] = segs[0]

set_printoptions(threshold='nan') 

def shiTest(class_flag):
	docList = []; classList = []; fullText = []
	trainMat = []
	for line in open("data/test_data"):
		line = line.rstrip("\n")

		content,classflag = line.split("\t")
		wordlist = textParse2(content)
		docList.append(wordlist)
		fullText.extend(wordlist)
		classList.append(class_flag[classflag])
	
	vocabList = createVocabList(docList)

	for doc in docList:
		trainMat.append(bagOfWord2VecMN(vocabList, doc))
	
	pNVect, pNbusive = trainNB1(trainMat, classList, len(class_flag))

	output_stream_vocab = open("conf/big_dict_conf", "wa")
	line = ""
	for item in vocabList:
		line += item.encode("gbk") + "#"
	line = line.rstrip("#")
	output_stream_vocab.write(line + "\n")
	output_stream_vocab.flush()

	for key in pNVect:
		file_name= "conf/"+key
		np.savetxt(file_name,pNVect[key])

	output_stream_pNbusive = open("conf/pNbusive_conf", "wa")
	for key in pNbusive:
		val = str(pNbusive[key])
		line = "\t".join([key, val])
		output_stream_pNbusive.write(line+"\n")
	output_stream_pNbusive.flush()


def load_pNVect_Conf():
	pNVect_dict = {};file_list = [];

	for line in open("conf/key"):
		file_list.append(line.rstrip("\n"))

	for file in file_list:
		file_name = "conf/" + file
		pNVect_dict[file] = np.loadtxt(file_name)

	return pNVect_dict

def load_pNbusive_Conf():
	pNbusive_dict = {}
	for line in open("conf/pNbusive_conf"):
		line = line.rstrip("\n")
		key, val = line.split("\t")
		pNbusive_dict[key] = float(val)

	return pNbusive_dict

def load_big_dict_Conf():
	vocabList = []
	for line in open("conf/big_dict_conf"):
		line = line.rstrip("\n").decode('gbk')
		vocabList.extend(line.split('#'))

	return vocabList

def test_poetry(line, pNVect, pNbusive, vocabList):

	segs = line.rstrip("\n").split("\t")
	val = ""
	testEntry = ""
	if len(segs) == 2:
		testEntry, val = segs
	else:
		testEntry = segs[0]

	testlist = textParse2(testEntry)
	thisDoc = array(bagOfWord2VecMN(vocabList, testlist))
	shi_dict = classifyNB2(thisDoc, pNVect, pNbusive, len(class_flag))

	num = 1
	print line
	print "%s\t%s" % ("original", val)
	print "你的诗歌类型可能是:"
	for item in shi_dict:
		if num <= 3:
			key,val = item
			key = key.lstrip("p")
			print shi_type[key]
		num += 1
	print '#############################################'


pNVect = load_pNVect_Conf()
pNbusive = load_pNbusive_Conf()
vocabList = load_big_dict_Conf()
for line in open("data/test"):
	test_poetry(line, pNVect, pNbusive, vocabList)
#shiTest(class_flag)
