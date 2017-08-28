#!/usr/bin/env python
#coding=gbk

from numpy import *
import numpy as np
set_printoptions(threshold='nan') 


class Handler_query():
	def __init__(self):
		self.class_flag = self.load_class_flag()
		self.shi_type = self.load_type_category()

		self.pNVect = self.load_pNVect_Conf()
		self.pNbusive = self.load_pNbusive_Conf()
		self.vocabList = self.load_big_dict_Conf()
		
	def load_class_flag(self):
		class_flag = {}
		num = 0
		for line in open("conf/category"):
			line = line.rstrip("\n")
			if line in class_flag:
				continue
			else:
				class_flag[line] = num
				num += 1

		return class_flag

	def load_type_category(self):
		shi_type = {}
		for line in open('conf/type_category'):
			line = line.rstrip("\n")
			segs = line.split("\t")
			shi_type[segs[1]] = segs[0]
		return shi_type
		
	def bagOfWord2VecMN(self,vocabList, inputSet):
		returnVec = [0]*len(vocabList)
		for word in inputSet:
			if word in vocabList:
				returnVec[vocabList.index(word)] += 1
			else:
				print "the word: %s is not in my Vocabulary!" % word
		return returnVec

	def classifyNB2(self,vec2Classify, pNVect, pNbusive, num):
		pN = {}
		for i in range(num):
			key = "p" + str(i) + "Vect"
			key2 = "p" + str(i) + "busive"
			key3= "p" + str(i)
			pN[key3] = sum(vec2Classify * pNVect[key] + log(pNbusive[key2]))
		return sorted(pN.iteritems(), key=lambda d:d[1], reverse=True)

	def textParse2(self, string):
		import jieba
		return jieba.lcut(string)
	
	def load_pNVect_Conf(self):
		pNVect_dict = {};file_list = [];

		for line in open("conf/key"):
			file_list.append(line.rstrip("\n"))

		for file in file_list:
			file_name = "conf/" + file
			pNVect_dict[file] = np.loadtxt(file_name)

		return pNVect_dict

	def load_pNbusive_Conf(self):
		pNbusive_dict = {}
		for line in open("conf/pNbusive_conf"):
			line = line.rstrip("\n")
			key, val = line.split("\t")
			pNbusive_dict[key] = float(val)

		return pNbusive_dict

	def load_big_dict_Conf(self):
		vocabList = []
		for line in open("conf/big_dict_conf"):
			line = line.rstrip("\n").decode('gbk')
			vocabList.extend(line.split('#'))

		return vocabList

	def test_poetry(self,line):

		segs = line.rstrip("\n").split("\t")
		val = ""
		testEntry = ""
		if len(segs) == 2:
			testEntry, val = segs
		else:
			testEntry = segs[0]

		testlist = self.textParse2(testEntry)
		thisDoc = array(self.bagOfWord2VecMN(self.vocabList, testlist))
		shi_dict = self.classifyNB2(thisDoc, self.pNVect, self.pNbusive, len(self.class_flag))
		result = ""
		num = 1
		for item in shi_dict:
			if num <= 3:
				key,val = item
				key = key.lstrip("p")
				result += self.shi_type[key]
			num += 1
		return result



#handler = Handler_query()
#line="出耘田夜绩麻，村庄儿女各当家童孙未解供耕织，也傍桑阴学种瓜"
#handler.test_poetry(line)

