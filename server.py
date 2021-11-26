from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from form import FormCreator
from random import randint
from fuseki import FusekiHandler
from id import IDGenerator
from journal_creator import JournalCreator

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1010
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

			# get_form_n_gears is static html string
			out = head+"""
			<body>
				<section>
					<h1>Welcome to</h1>
					<h2>GEAR 10 Productions</h2>
					<h3>GearBox - building [1/2]</h3>
					"""+FormCreator.get_form_n_gears+"""
				</section>
			</body>
			"""

			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/image.png") != -1:
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "image/png")
			s.end_headers()
			try:
				# Read the file
				bReader = open("./Product_images/"+str(photo_name)+".png", "rb")
				print("bReader ok")
				s.wfile.write(bReader.read())
				print("bReader read")
			except:
				# File not found
				print("except")
				msg = "Tester." # The gearbox was found in the database, but a photo has not yet been created.	Our magnificent Johanne is working hard to make a photo of it available ASAP
				print(msg)
				s.wfile.write(bytes(msg, 'utf-8'))
				print("except written")

		elif path.find("/favicon_10.ico") != -1:
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "image/x-icon")
			s.end_headers()
			#Read the file
			#Write file.
			bReader = open("./style_fav/favicon_10.ico", "rb")
			theImg = bReader.read()
			s.wfile.write(theImg)

		elif path.find("/style.css") != -1:
			# Make right headers
			s.send_response(200)
			s.send_header("Content-type", "text/css")
			s.end_headers()
			#Read the file
			#Write file.
			bReader = open("./style_fav/style.css", "rb")
			theImg = bReader.read()
			s.wfile.write(theImg)

		else:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

			if path.find("/reciept") != -1:
			# Special message to making GET call to /reciept
				out = head+"""
				<body> 
					<section>
						<h1>Aii, you can't do that! The order was made but now you lost your reciept! </h1><br>\
					</section>
					<a href="/"><button>Make another!</button></a>
				</body></html>"""
			else:
				out = head+"""
				<body>
					<p>
						The path: " """+ path + """ "
						has not been implemented as a GET method.
						Start from start page!
					</p>
					<a href="/"><button>Go back</button></a>
				</body></html>"""
			s.wfile.write(bytes(out, "utf-8"))


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

			out = head+"""
			<body>
				<section>
					<h1>GearBox - building [2/2]</h1>
					"""+ FormCreator.get_form_set_radiuses(n_gears)+"""
				</section>
				<a href="/"> <button>Go back</button> </a> </body>"""
			s.wfile.write(bytes(out, 'utf-8'))

		elif path.find("/review") != -1:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()

			# Reset list of radiuses
			radius_list = []

			# Get the arguments from previous page
			content_len = int(s.headers.get('Content-Length'))
			pairs = s.rfile.read(content_len)\
				.decode()\
					.split("&")
			n_gears = len(pairs)

			# Making radius list for the requested gear box
			for i in range(0, n_gears):
				radius_list.append(int(pairs[i].split("=")[1]))

			out = head+"""<body><section><h1>GearBox - review </h1>
					""" + str(n_gears) + " gears chosen. Radiuses are as follows:<br><br>"
			for i in range(n_gears):
				out += ("Gear nr." + str(i+1) + ": " + str(radius_list[i]) + " [mm]<br>")
			out += "<a href='/'><button>Go back</button></a><br><br>"
			
			try:
				if (FusekiHandler.is_gearBox_in_db(radius_list) != 0):
					# Looking for photo of the gear box
					photo_name = FusekiHandler.get_photo_name_from_db(radius_list)
					if photo_name == "":
						# photoname er ikke laget
						out += """The gearbox was found in the database, but a photo has not yet been created. 
								Our magnificent Johanne is working hard to make a photo of it available ASAP."""
					else:
						# Photo name ligger i databasen!
						# Supply the photo
						out += """<img 
							src="/image.png" 
							alt= "The gearbox was found in the database, but a photo has not yet been created. 
								Our magnificent Johanne is working hard to make a photo of it available ASAP."
								width="500">"""
				else:
					# Gear box er ikke i databasen, lager journal fil
					photo_name = IDGenerator.create_photo_name(radius_list)
					JournalCreator.create_gear_box_journal_file(radius_list, photo_name)
					out += """The gearbox was not found in the database, but is now being created. We will supply it when it is ready. <br>
						Our magnificent Johanne is working hard to make a photo of it available ASAP."""
					FusekiHandler.add_gearBox_to_db_rad(radius_list)
					FusekiHandler.add_photo_name_to_gearbox(radius_list, photo_name)
					
			except Exception as e:
				# Print future error messages.
				print(e)
				out += "Something went wrong"

			# Skjema for bestilling
			form = FormCreator.get_form_private_customer_DUMMY(radius_list)
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

			# [Name, address, phone, email, material, color, photoname, [radius_list]]
			form_input_list = [pairs[i].split("=")[1] for i in range(len(pairs))]
			form_input_list = ServerHandler.make_form_input_normal_again(form_input_list)
			out = head+"<body><section>"+ServerHandler.get_personalized_message(form_input_list)\
			+"""<br>
				... Disclaimer: Unfortunately, this is only a school project so estimated delivery is NEVER...<br>
			</section><br><a href="/"><button>Make another!</button></a></body>
			""" + ServerHandler.create_reciept(form_input_list)
			s.wfile.write(bytes(out, 'utf-8'))	
			FusekiHandler.create_order(form_input_list)
		
		else:
			s.send_response(200)
			s.send_header("Content-type", "text/html")
			s.end_headers()
		
			out = head + "<body><p>The path: " + path + """ 
				has not been implemented as a GET method.
				Start from start page!</p> <a href="/"><button>Go back</button></a><br><br>
				</body></html>"""
			
			s.wfile.write(bytes(out, "utf-8"))

	def create_header():
		# Returns a header
		# fav = '<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>'
		return	"""
			<HTML lang="en"> 
			<head>
				<title> Gear 10 </title>
				<link rel="icon" href="/favicon_10.ico" type="image/x-icon"/>
				<link rel="stylesheet" href="/style.css">
			</head>
			"""
			

	def get_personalized_message(form_input_list):
		# customer has now been added to db with the current order, and therefore everyone is in db at this point, with >0 orders
		try:
			n_orders = FusekiHandler.count_customer_orders(form_input_list)
			if n_orders >= 1:
				return "<h3>WELCOME BACK OL' PAL! You now have "+str(n_orders)+" orders!</h3>"
			else:
				return "<h3>WELCOME NEW CUSTOMER! <br>Your first gear box is ordered.</h3><br>"
		except:
			return "Order successfully added!<br>"

	def make_form_input_normal_again(form_input_list):
		# RETURNS [name, address, phone, email, material, color, "", [radiuses]]
		string_input_list = (str(form_input_list[i])\
			.replace("+", " ").replace("%40", "@").replace("%21", "!")\
				.replace("%3D", "=").replace("%3F", "(").replace("%28", "(")\
					.replace("%29", ")").replace("%0D", "<br>").replace("%0A", "<br>")\
						.replace("%5B", "[").replace("%2C", ",").replace("%5D", "]") \
							.replace("%22", "").replace("%F8", "ø")
							for i in range(len(form_input_list)))
		# Yes I have tried to fix this but no luck.
		# print("STR:"+ unquote(next((str(x) for x in form_input_list))))
		name = next(string_input_list)
		address = next(string_input_list)
		phone = next(string_input_list)
		email = next(string_input_list)
		material = next(string_input_list, "Unspecified")
		color = next(string_input_list, "Unspecified")
		radiuses = next(string_input_list)
		form_input_list_readable = [name, address, phone, email, material, color, "", radiuses]
		return form_input_list_readable

	def create_reciept(form_input_list):
		form_input_list_readable = form_input_list
		reciept = """
				<section>
					<h1> ----------------------- ORDER SUMMARY ----------------------- </h1>
					Name: """+form_input_list_readable[0]+ """<br>
					Address: """+form_input_list_readable[1]+ """<br>
					Phone: """+form_input_list_readable[2]+ """<br>
					Email: """+form_input_list_readable[3]+ """<br><br>
					"""+ ServerHandler.get_printable_radiuses(form_input_list_readable[7])+"""
					Material: """
		material = form_input_list_readable[4]
		if IDGenerator.get_material_number(material) == 3:
			# Diamonds are requested, but are they available?
			if ServerHandler.is_diamond_available():
				reciept += material+""", and diamonds ARE luckily(!) available at the moment!<br>"""
			else:
				reciept += material + """, but those are unluckily not available at the moment...<br>"""
		else:
			reciept += material+"""<br>"""

		reciept += """Color: """+form_input_list_readable[5] + """<br><br>
					<h3>Thank you for shopping at Gear 10 Productions. Hope the gear box suits your gearing needs. You can pay later!</h3>
				</section>"""
		return reciept

	def get_printable_radiuses(string_gear_radius_list):
		# Make a list instead of string
		gear_radius_list = string_gear_radius_list[1:-1].split(",")
		out = str(len(gear_radius_list))
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


