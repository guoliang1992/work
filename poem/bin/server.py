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

	def do_GET(self):                     #响应GET请求)
		url_param = self.path
		line = unquote(url_param.lstrip("/query=")).encode('gbk')
		type_poem = handler.test_poetry(line)
		print "%s\t%s\t" % (type_poem, line)
		query_word = type_poem+line
		result = es_tools.get_img(query_word)
		if result =="":
			result = "http://img02.sogoucdn.com/app/a/200773/19026f5bb9fbf86647fb207fd4f9ad8c#^^^#http://img04.sogoucdn.com/app/a/200773/8fc984dfeb78be8b3f6547e100a5cfc4#^^^#http://img01.sogoucdn.com/app/a/200773/68b329da9893e34099c7d8ad5cb9c940"

		enc="UTF-8"
		self.send_response(200)           #发送200状态码，表示处理正常)
		self.send_header("Content-type", "text/html; charset=%s" % enc)   

		self.send_header("Content-Length", str(len(result)))    
		self.end_headers()                #html头部分结束
		self.wfile.write(result)            #以刚才读出的那个文件的内容作为后续内容发出给http客户端

handler = Handler_query()
es_tools = DB_Tools()
httpd=HTTPServer(("", 8383), MyHttpHandler) 
print("Server started port 8383….")
httpd.serve_forever()  #启动http服务器2017/8/25 15:30:26)))))))))

