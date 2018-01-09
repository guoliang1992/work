#!/usr/bin/env python
#coding:gbk

import requests, random
import os, sys, time
from bs4 import BeautifulSoup
import json
star_dict = {'allstar10':'1','allstar20':'2','allstar30':'3','allstar40':'4','allstar50':'5','':'3'}
def crawer_page(original_url, retry = 1, referer='https://movie.douban.com/'):
	hds=['Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36']
	cookie = 'bid=CDCpAVUsTgo; gr_user_id=a4690ed3-8e73-4806-95b0-48bed8515c4a; viewed="3695850_24703171_10769749_2061116"; ps=y; __yadk_uid=Dfy68FmyPYCQjoPmmmWackaMeVdWtR38; ct=y; ap=1; ll="108288"; __utmt=1; dbcl2="159629853:ux0NwYWDJr0"; ck=niA1; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1515401862%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _vwo_uuid_v2=5EB23EABB6AB7EF68C051F39D24B4E63|ac95dd92e131cf1422f13b12b0e8d411; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=4b134295804c062b.1515139107.5.1515401977.1515398517.; _pk_ses.100001.4cf6=*; __utma=30149280.506436274.1511245070.1515395479.1515401497.9; __utmb=30149280.3.10.1515401497; __utmc=30149280; __utmz=30149280.1515119028.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.15962; __utma=223695111.965785939.1515139107.1515395479.1515401862.5; __utmb=223695111.0.10.1515401862; __utmc=223695111; __utmz=223695111.1515401862.5.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login'
	headers = {'User-Agent' : hds[0],'Referer':referer, 'Cookie':cookie}

	t = 0
	time.sleep(3)
	while t < retry:
		try:
			data = requests.get(original_url, headers=headers, verify=False)
			return data.content
		except:
			t +=1
			time.sleep(0.5 * t)
	return ''

def parse_content(movie_id, page_content):
	soup = BeautifulSoup(page_content, 'html.parser')
	for tab in soup.select('.sub_ins table'):
		try:
			url = tab.select('tr td a')[0]['href']
			name = tab.select('.pl2')[0].get_text().split(' ')[0].strip()
			star = tab.select('.pl span')[0]['class'][0]
			info = [movie_id,url, name, star_dict[star]]
			print '\t'.join(info).encode('gbk')
		except Exception, e:
			print e
			pass


if __name__ == '__main__':
	filename = sys.argv[1]
	for line in open(filename):
		url = line.rstrip('\n')
		movie_id = url.split('/')[-2]
		page = crawer_page(url)
		parse_content(movie_id, page)
