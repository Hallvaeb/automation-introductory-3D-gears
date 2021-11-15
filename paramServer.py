#paramServer.py
#HTTP Server template / One parameter
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import sys


HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1234

#file path of this python file
filePath = 'C:/Users/Eier/OneDrive/Studier/TMM4270/python'

# Handler of HTTP requests / responses
class MyHandler(BaseHTTPRequestHandler):
	


	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	
	def do_GET(s):
		"""Respond to a GET request."""
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		if path.find("/") != -1 and len(path) == 1:
			s.wfile.write(bytes('<html lang="en"> <title> Gearbox </title></head>', 'utf-8'))
			s.wfile.write(bytes('<section><h2>GearBox - building [1/2]</h2><form action = "/setRadius" method="post">', 'utf-8'))
			s.wfile.write(bytes('<label for="nGears">How many gears do you want?</label><br>', 'utf-8'))
			s.wfile.write(bytes('<input type="number" name="nGears" id="nGears" autofocus value = "2">', 'utf-8'))
			s.wfile.write(bytes('<input type="submit" value="submit"><br>', 'utf-8'))
			s.wfile.write(bytes('</form></section>', 'utf-8'))

		else:
			s.wfile.write(bytes('<html><head><title>Cool interface.</title></head>', 'utf-8'))
			s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
			s.wfile.write(bytes('</body></html>', "utf-8"))
			
	def do_POST(s):

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		path = s.path
			
		if path.find("/setRadius") != -1:
			# Get nGears variable
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			nGears = param_line.split("=")[1]
			print("nGears: ", nGears)

			# HTML title ++
			s.wfile.write(bytes('<html lang="en"> <title> Gearbox </title></head>', 'utf-8'))
			s.wfile.write(bytes('<title> Gearbox </title></head>', 'utf-8'))
			s.wfile.write(bytes('<section><h1>GearBox - building [2/2]</h1><form action = "/review" method="post">', 'utf-8'))
			s.wfile.write(bytes(nGears+' gears chosen! Choose the radiuses:<br><br>', 'utf-8'))
			
			# Making a field for each gear radius
			for i in range(int(nGears)): # nGears
					s.wfile.write(bytes('<label for="gear"'+str(i)+'> Gear '+str(i+1)+":"+'</label>', 'utf-8'))
					s.wfile.write(bytes('<input id = '+str(i)+' name = '"gear"+str(i)+' placeholder = "Radius [mm]" required> <br><br>', 'utf-8'))
			# s.wfile.write(bytes('<input name = "nGears" value = str(nGears) </input>', 'utf-8'))
		
			# Making the buttons
			s.wfile.write(bytes('<input type="submit" value="submit">', 'utf-8'))
			s.wfile.write(bytes('</form></section>', 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a>', 'utf-8'))

		elif path.find("/review") != -1:
			# Reset list of radiuses
			radius_list = []

			# Get the arguments
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			pairs = param_line.split("&")
			nGears = len(pairs)
			for i in range(0, nGears):
				radius_list.append(int(pairs[i].split("=")[1]))

			# Write up the page
			out = """<html lang="en"> <title> Gearbox </title></head><title> Gearbox </title></head>
					<section><h1>GearBox - review </h1><form action = "/accept" method="post">
					nGears+' gears chosen. Radiuses are as follows:<br><br>"""
			for i in range(radius_list):
				out += ('Gear '+str(i)+': '+radius_list[i]+'\n')
			s.wfile.write(bytes(out, 'utf-8'))
			
			
 
if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

