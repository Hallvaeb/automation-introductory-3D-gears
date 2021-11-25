from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from form import FormCreator
from random import randint
from fuseki import FusekiHandler
from id import IDGenerator
from journal_creator import JournalCreator

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1234
photo_name = "default"


class ServerHandler(BaseHTTPRequestHandler):


	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	
	def do_GET(s):
		"""Respond to a GET request."""

		head = ServerHandler.create_header()
		global photo_name

		path = s.path
		if path.find("/") != -1 and len(path) == 1:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

			out = head+"""
			<body>
				<section>
				
					<h1>Welcome to</h1>
					<h2>GEAR 10 Productions</h2>
					<h3>GearBox - building [1/2]</h3>
					
					<form action = '/setRadius' method='post'>
						<label for='n_gears'>How many gears do you want?</label><br><br>
						<input pattern='0123456789' type='number' name='n_gears' id='n_gears' autofocus required><br><br>
						<input type='submit' value='submit'><br>
					</form>

				</section>
			</body>
			"""
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/reciept") != -1:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()
		
			thankyou = head+"""
			<body> <section><h1>Aii, you can't do that! The order was made but now you lost your reciept! </h1><br>
			"""
			s.wfile.write(bytes(thankyou, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Make another!</button></a></body>', 'utf-8'))

		elif path.find("/image.png") != -1:
			print("Image is being accessed:", photo_name)
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "image/png")
			s.end_headers()
			#Read the file
			bReader = open("./Product_images/"+str(photo_name)+".png", "rb")
			#Write file.
			theImg = bReader.read()
			s.wfile.write(theImg)

		# elif path.find("/favicon_10.ico") != -1:
		# 	# Make right headers
		# 	s.send_response(200)
		# 	s.send_header("Content-type", "image/x-icon")
		# 	s.end_headers()
		# 	#Read the file
		# 	#Write file.
		# 	bReader = open("./style_fav/favicon_10.ico", "rb")
		# 	theImg = bReader.read()
		# 	s.wfile.write(theImg)

		# elif path.find("/style.css") != -1:
		# 	# Make right headers
		# 	s.send_response(200)
		# 	s.send_header("Content-type", "text/css")
		# 	s.end_headers()
		# 	#Read the file
		# 	#Write file.
		# 	bReader = open("./style_fav/style.css", "rb")
		# 	theImg = bReader.read()
		# 	s.wfile.write(theImg)

		else:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()
		
			s.wfile.write(bytes(head, 'utf-8'))
			s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
			s.wfile.write(bytes('</body></html>', "utf-8"))


	def do_POST(s):

		global photo_name

		head = ServerHandler.create_header()
		path = s.path
			
		if path.find("/setRadius") != -1:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

			# Get n_gears variable
			content_len = int(s.headers.get('Content-Length'))
			n_gears = s.rfile.read(content_len)\
				.decode()\
					.split("=")[1]

			# HTML title ++
			out = head+"""<body>
			<section><h1>GearBox - building [2/2]</h1>
			<form action = "/review" method="post">
			"""+str(n_gears)+""" 
			gears chosen! Choose the radiuses:<br><br>
			"""			
			# Making a field for each gear radius
			for i in range(int(n_gears)): # n_gears
					out += "<label for='gear'" + str(i) + "> Gear " + str(i+1) + ": </label>"
					out +="""
					<input type = "number" pattern="0123456789" id = '""" + str(i) + """' 
						name = '"gear" """ + str(i) +""" ' placeholder = "Radius [mm]" 
						autofocus> <br><br> """
							
			# Making the buttons
			out += """<input type="submit" value="Submit">\
					<a href="/"> <button>Go back</button> </a> </body>\
						</form></section>"""
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/review") != -1:
			# IN POST
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

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

			# Write the page 
			out = head+"""<body><section><h1>GearBox - review </h1>
					""" + str(n_gears) + ' gears chosen. Radiuses are as follows:<br><br>'
			for i in range(n_gears):
				out += ('Gear nr.' + str(i+1) + ': ' + str(radius_list[i]) + ' [mm]<br>')
			out += '<a href="/"><button>Go back</button></a><br><br>'

			try:
				photo_name = IDGenerator.create_photo_name(radius_list)
				if (FusekiHandler.is_gearBox_in_db(radius_list) != 0):
					FusekiHandler.add_photo_name_to_gearbox(radius_list, photo_name)
					out += '<img src="/image.png" alt= "The gearbox was still found in the database, but a photo has not yet been created. Our magnificent Johanne is working hard to make a photo of it available ASAP.">'
				else:
					response = JournalCreator.create_gear_box_journal_file(radius_list, photo_name)
					if(response):
						out += "The gearbox was not found in the database. We will supply it when it is ready. Our magnificent Johanne is working hard to make a photo of it available ASAP."
					FusekiHandler.add_gearBox_to_db_rad(radius_list)
			except Exception as e:
				print(e)
				out += "Something went wrong"

			# Skjema for bestilling
			form = FormCreator.create_form_private_customer_DUMMY(radius_list)
			out += form+"</body>"
			s.wfile.write(bytes(out, 'utf-8'))
		
		elif path.find("/reciept") != -1:

			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

			# Get the arguments
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			pairs = param_line.split("&")

			# [Name, address, phone, email, material, color, photoname, radius_list[]]
			form_input_list = [pairs[i].split("=")[1] for i in range(len(pairs))]

			out = head+"<body>"+ServerHandler.get_personalized_message(form_input_list)\
			+"""
			<section>
				... Disclaimer: Unfortunately, this is only a school project so estimated delivery is NEVER...<br>
			</section><br>
			"""
			s.wfile.write(bytes(out, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Make another!</button></a>', 'utf-8'))
			
		
			reciept = ServerHandler.create_reciept(form_input_list)
			s.wfile.write(bytes(reciept, 'utf-8'))
			
			# [Name, address, phone, email, material, color, radius_list[]]
			# FusekiHandler.add_order_to_db(form_input_list)
			s.wfile.write(bytes("</body>", 'utf-8'))

	def create_header():
		# Returns a header
		# fav = '<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>'
		return	"""
			<HTML lang="en"> 
			<head>
				<title> Gear 10 </title>
				<link rel="icon" href="/favicon_10.ico" type="image/x-icon"/>
				
			</head>
			"""#<link rel="stylesheet" href="/style.css">

	def get_personalized_message(form_input_list):
		print(form_input_list)
		print("personalized msg")
		# customer has now been added to db with the current order, and therefore everyone is in db at this point, with >0 orders
		try:
			print("Finner N ORDERS FROM COUNT CUSTOMER ORDERS")
			n_orders = FusekiHandler.count_customer_orders(form_input_list)
			print(n_orders, "N ORDERS FROM COUNT CUSTOMER ORDERS")
			if n_orders > 1:
				return "WELCOME BACK OL' PAL! You now have "+str(n_orders)+"!"
			else:
				return "WELCOME NEW CUSTOMER! You just made your first order (at least on this email).<br>"
		except:
			return "Order successfully added!<br>"

	def create_reciept(form_input_list):
		# Remove weird signs in inefficient but functional way
		# ASCII to utf-8 eller character
		string_input_list = (str(form_input_list[i]).\
			replace("+", " ").replace("%40", "@").replace("%21", "!")\
				.replace("%3D", "=").replace("%3F", "(").replace("%28", "(")\
					.replace("%29", ")").replace("%0D", "<br>").replace("%0A", "<br>")\
						.replace("%5B", "[").replace("%2C", ",").replace("%5D", "]") \
							.replace("%22", "")
							for i in range(len(form_input_list)))
		# Yes I have tried to fix this but no luck.
		# print("STR:"+ unquote(next((str(x) for x in form_input_list))))
		reciept = """
				<section>
					<h1> ----------------------- ORDER SUMMARY ----------------------- </h1>
					Name: """+next(string_input_list)+ """<br>
					Address: """+next(string_input_list)+ """<br>
					Phone: """+next(string_input_list)+ """<br>
					Email: """+next(string_input_list)+ """<br><br>
					"""+ServerHandler.get_printable_radiuses(next(string_input_list))+"""
					Material: """
		material = next((string_input_list), "Unspecified")
		if IDGenerator.get_material_number(material) == 3:
			# Diamonds are requested, but are they available?
			if ServerHandler.is_diamond_available():
				reciept += material+""", and diamonds ARE luckily(!) available at the moment!<br>"""
			else:
				reciept += material + """, but those are unluckily not available at the moment...<br>"""
		else:
			reciept += material+"""<br>"""

		reciept += """Color: """+next((string_input_list), "Unspecified")+ """<br><br>
					<h3>Thank you for shopping at Gear 10 Productions. Hope the gear box suits your gearing needs. You can pay later!</h3>
				</section>"""
		return reciept

	def get_printable_radiuses(string_gear_radius_list):
		"""
		input: gear radius list in string form
		output: returns the radiuses in a nice looking fashion
		"""
		# Make a list instead of string
		gear_radius_list = string_gear_radius_list[1:-1].split(",")

		out = str(len(gear_radius_list))
		# try:
		# 	if(FusekiHandler.is_gearBox_in_db(gear_radius_list)):
		# 		out += ' gears are already created and on their way! Radiuses are as follows:<br>'
		# 	else:
		# 		out += ' gears are being created by brilliant college student Johanne. Radiuses are as follows:<br>'
		# except:
		out += ' gears are ordered. Radiuses are as follows:<br>'

		for i in range(len(gear_radius_list)):
			out += ('Gear nr.' + str(i+1) + ': ' + str(gear_radius_list[i]) + ' [mm]<br>')
		return out

	def is_diamond_available():
		if randint(0,9) > 4:
			return 0
		return 1


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


