# -*- coding: UTF-8 -*-

import sys
import re

#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import shutil  
from urllib import unquote
from find_img import Handler_query
from es_DB import DB_Tools
class MyHttpHandler(BaseHTTPRequestHandler):

	def do_GET(self):                     #��ӦGET����)
		url_param = self.path
		line = unquote(url_param.lstrip("/query=")).encode('gbk')
		type_poem = handler.test_poetry(line)
		print "%s\t%s\t" % (type_poem, line)
		query_word = type_poem+line
		result = es_tools.get_img(query_word)
		if result =="":
			result = "http://img02.sogoucdn.com/app/a/200773/19026f5bb9fbf86647fb207fd4f9ad8c#^^^#http://img04.sogoucdn.com/app/a/200773/8fc984dfeb78be8b3f6547e100a5cfc4#^^^#http://img01.sogoucdn.com/app/a/200773/68b329da9893e34099c7d8ad5cb9c940"

		enc="UTF-8"
		self.send_response(200)           #����200״̬�룬��ʾ��������)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   

		self.send_header("Content-Length", str(len(result)))    
		self.end_headers()                #htmlͷ���ֽ���
		self.wfile.write(result)            #�ԸղŶ������Ǹ��ļ���������Ϊ�������ݷ�����http�ͻ���

handler = Handler_query()
es_tools = DB_Tools()
httpd=HTTPServer(("", 8383), MyHttpHandler) 
print("Server started port 8383��.")
httpd.serve_forever()  #����http������2017/8/25 15:30:26)))))))))

