#!/user/bin/env python
#coding:gbk

import json
from datetime import datetime
from elasticsearch import Elasticsearch
import elasticsearch.helpers
from elasticsearch import helpers  

es = Elasticsearch('xxx:9200')
actions = []

path="tmp/data_dict"
num = 0
try:
	for line in open(path):
		line = line.rstrip("\n")

		if num %1000 == 0:
			print num
		action={
			"_index" : 'poem',
			"_type" : 'poems',
			"_id" : num,
			"_source" : line
		}
		num += 1
		actions.append(action)
		
		if len(actions) == 10000:
			helpers.bulk(es, actions)
			del actions[0 : len(actions)]

	if len(actions) > 0:
		helpers.bulk(es, actions)
		#es.index(index="infocenter", doc_type="weixin",body=line)
except Exception, e:
	print e
	pass
