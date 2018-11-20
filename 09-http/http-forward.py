#!/usr/bin/python3

import sys
import http

port = int(sys.argv[1])
upstream = sys.argv[2]
from http.server import BaseHTTPRequestHandler,HTTPServer
from http.client import HTTPConnection

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		httpconnection = HTTPConnection(upstream,timeout=1)
		httpconnection.request("GET",upstream)
		r1 = httpconnection.getresponse()
		print(r1.status,r1.reason)
		# self.request()
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write(bytes("Hello World !\n","utf8"))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', port), myHandler)
	print('Started httpserver on port ' , port)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()