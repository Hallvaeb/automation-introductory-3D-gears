from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from form import FormCreator
from fuseki import FusekiHandler

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1234


class ServerHandler(BaseHTTPRequestHandler):

	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	
	def do_GET(s):
		"""Respond to a GET request."""
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		head = ServerHandler.create_header()
		
		path = s.path
		if path.find("/") != -1 and len(path) == 1:
			site = head+"""
			<section>
				<h2>GearBox - building [1/2]</h2>
				<form action = "/setRadius" method="post">
					<label for="n_gears">How many gears do you want?</label><br><br>
					<input pattern="0123456789" type="number" name="n_gears" id="n_gears" autofocus required><br><br>
					<input type="submit" value="submit"><br>
				</form>
			</section>
			"""
			s.wfile.write(bytes(site, 'utf-8'))

		# elif path.find("/favicon_10.ico") != -1:
		# 	s.wfile.write(bytes(fav,'utf-8'))
			
		elif path.find("/review") != -1:
			# Reset list of radiuses
			radius_list = [50, 100, 150]

			n_gears = len(radius_list)

			# Write up the page
			out = head+"""<section><h1>GearBox - review </h1>
					""" + str(n_gears) + ' gears chosen. Radiuses are as follows:<br><br>'
			for i in range(n_gears):
				out += ('Gear nr.' + str(i+1) + ': ' + str(radius_list[i]) + ' [mm]<br>')
			s.wfile.write(bytes(out, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a><br><br>', 'utf-8'))

			try:
				gearBox_photo_path = "" #FusekiRequest.get_photo_path_from_db(radius_list)
				if(gearBox_photo_path != "-1"):
					s.wfile.write(bytes('<img src="./Product_images/test.jpg" alt= "Photo missing...">', 'utf-8'))
				else:
					s.wfile.write(bytes('The gearbox was not found in the database. We will supply it when it is ready.', 'utf-8'))
			except:
				s.wfile.write(bytes("Something went wrong", 'utf-8')) #'That gearbox would\'ve been too cool for the program to display it.'

			# Skjema for bestilling
			form = FormCreator.create_form_private_customer()
			s.wfile.write(bytes(form, 'utf-8'))

		elif path.find("/reciept") != -1:
			thankyou = head+"""
			<section><h1>outdated Thank you! Your ordered has been registered! </h1>
			... Disclaimer: Unfortunately, this is only a school project so estimated delivery is NEVER...<br>
			"""
			s.wfile.write(bytes(thankyou, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Make another!</button></a>', 'utf-8'))

		else:
			s.wfile.write(bytes(head, 'utf-8'))
			s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
			s.wfile.write(bytes('</body></html>', "utf-8"))


	def do_POST(s):

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		head = ServerHandler.create_header()
		
		path = s.path
			
		if path.find("/setRadius") != -1:
			# Get n_gears variable
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			n_gears = param_line.split("=")[1]

			# HTML title ++
			s.wfile.write(bytes(head, 'utf-8'))
			s.wfile.write(bytes('<section><h1>GearBox - building [2/2]</h1>', 'utf-8'))
			s.wfile.write(bytes('<form action = "/review" method="post">', 'utf-8'))
			s.wfile.write(bytes(n_gears + ' gears chosen! Choose the radiuses:<br><br>', 'utf-8'))
			
			# Making a field for each gear radius
			for i in range(int(n_gears)): # n_gears
					s.wfile.write(bytes('<label for="gear"' + str(i) + '> Gear ' + str(i+1) + ': </label>', 'utf-8'))
					s.wfile.write(bytes('<input type = "number" pattern="0123456789" id = ' + str(i) + ' name = '"gear" + str(i) + ' placeholder = "Radius [mm]" required autofocus> <br><br>', 'utf-8'))
							
			# Making the buttons
			s.wfile.write(bytes('<input type="submit" value="submit">', 'utf-8'))
			s.wfile.write(bytes('</form></section>', 'utf-8'))
			# Has to be outside form, pushes it down on the page.
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a>', 'utf-8'))

		elif path.find("/review") != -1:
			# Reset list of radiuses
			radius_list = []

			# Get the arguments
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			pairs = param_line.split("&")
			n_gears = len(pairs)
			for i in range(0, n_gears):
				radius_list.append(int(pairs[i].split("=")[1]))

			# Write up the page
			out = head+"""<section><h1>GearBox - review </h1>
					""" + str(n_gears) + ' gears chosen. Radiuses are as follows:<br><br>'
			for i in range(n_gears):
				out += ('Gear nr.' + str(i+1) + ': ' + str(radius_list[i]) + ' [mm]<br>')
			s.wfile.write(bytes(out, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a><br><br>', 'utf-8'))

			try:
				gearBox_photo_path = FusekiHandler.get_photo_path_from_db(radius_list)
				if(gearBox_photo_path != "-1"):
					s.wfile.write(bytes('<img src="./Product_images/test.jpg" alt= "Photo missing...">', 'utf-8'))
				else:
					s.wfile.write(bytes('The gearbox was not found in the database. We will supply it when it is ready.', 'utf-8'))
			except:
				s.wfile.write(bytes("Something went wrong", 'utf-8')) #'That gearbox would\'ve been too cool for the program to display it.'

			# Skjema for bestilling
			form = FormCreator.create_form_private_customer()
			s.wfile.write(bytes(form, 'utf-8'))
		
		elif path.find("/reciept") != -1:
			thankyou = head+"""
			<section>
				<h1> Thank you! Your ordered has been registered! </h1>
				... Disclaimer: Unfortunately, this is only a school project so estimated delivery is NEVER...<br>
			</section><br>
			"""
			s.wfile.write(bytes(thankyou, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Make another!</button></a>', 'utf-8'))
			
			# Get the arguments
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			pairs = param_line.split("&")

			# [Company name, contact, phone, email, material, color, comments, radius_list[]]
			form_input_list = [pairs[i].split("=")[1] for i in range(len(pairs))]
			
			string_input_list = str(form_input_list).replace("+", " ").replace("%40", "@").replace("%21", "!").replace("%3D", "=").replace("%3F", "(").replace("%28", "(").replace("%29", ")").replace("%0D", "<br>").replace("%0A", "<br>")
			reciept = """
				<section>
					<h1> ----------------------- ORDER SUMMARY ----------------------- </h1>
					"""+string_input_list+ """<br><br>
					Hope you will be happy with your purchase... You can pay later!
				</section>"""

			s.wfile.write(bytes(reciept, 'utf-8'))
			
			FusekiHandler.add_order_to_db(form_input_list)

	def create_header():
		# Returns a header
		# fav = '<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>'
		return	"""
			<HTML lang="en"> 
			<head>
				<title> Gearbox</title>
				<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>
				<link rel="stylesheet" href="style.css">
			</head>
			"""

if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), ServerHandler)
	print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

# Valeria