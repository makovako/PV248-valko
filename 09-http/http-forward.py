#!/usr/bin/python3

import sys
import http
import json
from socket import timeout

port = int(sys.argv[1])
upstream = sys.argv[2]
from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib

class myHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		headers = dict(self.headers)
		request = urllib.request.Request(upstream)
		request.headers = headers
		request.method = 'GET'
		out = {}
		try:
			with urllib.request.urlopen(request,timeout=1) as response:
				out["code"] = response.status
				out["headers"]	= dict(response.getheaders())
				data = response.read()
				try:
					out["json"] = json.loads(data)
				except ValueError:
					out["content"] = data
		except timeout:
			out["code"] = "timeout"
		self.send_response(200)
		self.send_header("Content-Type",'application/json')
		self.end_headers()
		self.wfile.write(bytes(json.dumps(out, indent=4, ensure_ascii = False), 'UTF-8'))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', port), myHandler)
	# print('Started httpserver on port ' , port)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	# print ('^C received, shutting down the web server')
	server.socket.close()