#!/usr/bin/env python
#coding:gbk

import string
import re

class HandlerStr:
	def remove_special_character(self, check_str):
		new_str = u""
		for ch in check_str:
			
			#is character
			if u'\u4e00' <= ch <= u'\u9fff':
				new_str += ch

			#is number
			if ch >= u'\u0030' and ch<=u'\u0039':
				new_str += ch

			#is alphabet
			if (ch >= u'\u0041' and ch<=u'\u005a') or (ch >= u'\u0061' and ch<=u'\u007a'):
				new_str += ch
		return re.sub("[\s+\.\!\/_,$%^*(+\"\'|\t]+|[丨+——！，。？?、~@#￥%……&*（）]+".decode("gbk"), "".decode("gbk"), new_str)	
