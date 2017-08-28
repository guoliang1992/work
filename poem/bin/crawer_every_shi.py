#!/usr/env/bin python
#coding=gb2312

import requests, random
import os, sys, time
from bs4 import BeautifulSoup


def crawer_page(original_url, retry = 3):
	hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
	user_agent_index = random.randint(0,10) % len(hds)
	headers = hds[user_agent_index]

	time.sleep(1)
	t = 0

	while t < retry:
		try:
			data = requests.get(original_url, headers=headers)
			return data.content
		except Exception, e:
			print e
			if hasattr(e, 'code') and e.code == 404:
				return ''

			t += 1
			time.sleep(0.5 * t)
	return ''

def parse_content(page, flag_tag):
	soup = BeautifulSoup(page, "html.parser")
	a_tags = soup.select(".typecont span a")
	fix_url = "http://so.gushiwen.org"
	for atag in a_tags:
		url = atag['href'].encode('gbk', 'ignore') 
		if url.find("view") != -1:
			full_url = fix_url + url
			print '%s\t%s' % (full_url, flag_tag)
	

def to_line(page):
	return re.sub('[\r\n]','\t\t\t',page)

if __name__ == '__main__':
	for line in open("tags_url"):
		line = line.rstrip('\n')
		url,flag_tag = line.split("\t")
		content = crawer_page(url)
		parse_content(content, flag_tag)

	

