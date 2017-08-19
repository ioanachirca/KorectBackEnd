#!/usr/bin/python
import time
import cgi
import json
import os.path
import io
import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

"""
Scriptul MyServe.py ruleaza serverul de backend
El are ca parametri:
obligatorii:
Portul pe care va rula
optional:
Data pentru care este respectivele rupturi teoretice.
IP-ul bazei de date (default localhost)
Portul bazei de date (Default 3306)
"""

"""
Clasa HTTPServer ruleaza pe un singur thread ceea ce inseamna ca poate servi
dor un client la un moment dat, asa ca am creat o alta clasa care mosteneste
clasa HTTPServer dar pentru fiecare cerere(request) creeaza un thread care sa se
ocupe de ea
"""
class ThreadedHTTPServer(HTTPServer):
	def process_request(self, request, client_address):
		thread = Thread(target=self.__new_request, args=(self.RequestHandlerClass, request, client_address, self))
		thread.start()
	def __new_request(self, handlerClass, request, address, server):
		handlerClass(request, address, server)
		self.shutdown_request(request)
global PORT_NUMBER
"""
Datele default ale serverului
"""
HOST_NAME = '' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

"""
O  clasa care se va ocupa de cererile HTTP primite de serverul nostru
"""
class MyHandler(BaseHTTPRequestHandler):
	def do_POST(s):
		"""Respond to a POST request."""
		print "lala"
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "*")
		s.send_header("Access-Control-Expose-Headers", "Content-Disposition")

		"""
		Decodificare mesaj primit
		"""
		#ar fi dragut sa nu fie asa
		data_string = s.rfile.read(int(s.headers['Content-Length']))
		print  "ce primeste este " + data_string

		try:
			postvars = json.loads(data_string)
		except:
			print data_string.replace("%2F","/")
			data_string = data_string.replace("%2F","/")
			print data_string.split('&')
			a = data_string.split('&')
			d = dict(s.split('=') for s in a)
			print d
			postvars = d
		#ctype, pdict = cgi.parse_header(s.headers.getheader('content-type'))
		#if ctype == 'application/json':
		#	data_string = s.rfile.read(int(s.headers['Content-Length']))
		#	postvars = json.loads(data_string)
		#else:
		#	s.send_header("Content-type", "application/json")
		#	s.end_headers()
		#	postvars = {}
		#	s.wfile.write(json.dumps({"ERROARE":"NU E JSON"}))
		#	return
		#filtre extra le punem separat
		s.send_header("Content-type", "application/json")
		s.end_headers()
		print "trimite raspuns"
		result = {}
		result["date"] = "ioana"
		s.wfile.write(json.dumps(result))

	def do_HEAD(s):
		print "here"
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_OPTIONS(s):
		print "rahat"
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "*")
		s.send_header("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PUT")
		s.send_header("Access-Control-Allow-Headers", "content-disposition, content-type, authorization, cache-control, if-modified-since, pragma")
		#s.send_header("Access-Control-Allow-Headers", "*")
		s.end_headers()
	def do_GET(s):
		"""
		Respond to a GET request.
		Testare daca serverul de backend merge
		"""
		s.send_response(200)
		#FILENAME = s.path[1:len(s.path)]
		s.send_header("Content-type", "application/json")
		s.end_headers()
		s.wfile.write(json.dumps({"ERROARE":"NU MERGE CU GET PE AICI"}))
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python " + sys.argv[0] + " SERVER_PORT [DB_IP] [DB_PORT]"
		sys.exit(0)
	if len(sys.argv) >= 2:
		PORT_NUMBER = int(sys.argv[1])
	if len(sys.argv) >= 3:
		SQL_SERVER = str(sys.argv[2])
	if len(sys.argv) >= 4:
		SQL_PORT = int(sys.argv[3])
	"""
	Pornesc Serverul de HTTP care va rula pana va primi o intrerupere de la tastatura
	"""
	httpd = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
