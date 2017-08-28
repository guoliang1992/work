#!/usr/bin/env python
#coding:gbk
from handler_character import HandlerStr as handler_str

for line in open("gushi_content_flag"):
	try:
		line = line.rstrip("\n")
		content,tag = line.split("\t")
		content_ori = handler_str().remove_special_character(content.decode('gbk','ignore'))
		#print '%s\t%s' % (content_ori.encode('gbk'), tag)
	except Exception, e:
		print line
		print e
		pass
