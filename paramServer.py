#paramServer.py
#HTTP Server template / One parameter
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from fusekiRequest import FusekiRequest


HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1234

#file path of this python file
# filePath = 'C:/Users/Eier/OneDrive/Studier/TMM4270/python'

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
		
		fav = '<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>'
		head =	"""
			<HTML lang="en"> 
			<head>
				<title> Gearbox</title>
				<link rel="icon" href="./style_fav/favicon_10.ico" type="image/x-icon"/>
				<link rel="stylesheet" href="style.css">
			</head>
			"""
		
		# Check what the path is 
		path = s.path
		if path.find("/") != -1 and len(path) == 1:
			site = head+"""
			<section>
				<h2>GearBox - building [1/2]</h2>
				<form action = "/setRadius" method="post">
					<label for="nGears">How many gears do you want?</label><br><br>
					<input pattern="0123456789" type="number" name="nGears" id="nGears" autofocus required><br><br>
					<input type="submit" value="submit"><br>
				</form>
			</section>
			"""
			s.wfile.write(bytes(site, 'utf-8'))

		elif path.find("/favicon_10.ico") != -1:
			s.wfile.write(bytes(fav,'utf-8'))

		elif path.find("/reciept") != -1:
			thankyou = head+"""
			<section><h1>Thank you! Your ordered has been registered! </h1>
			... Disclaimer: Unfortunately, this is only a school project so estimated delivery is NEVER...<br>
			"""
			s.wfile.write(bytes(thankyou, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Make another!</button></a>', 'utf-8'))
			
		elif path.find("/review") != -1:
			# Reset list of radiuses
			radius_list = [50, 100, 150]
			nGears = len(radius_list)

			# Write up the page
			out = head+ """
					<section><h1>GearBox - review </h1>
					""" + str(nGears) + ' gears chosen. Radiuses are as follows:<br><br>'
			for i in range(nGears):
				out += ('Gear nr.' + str(i) + ': ' + str(radius_list[i]) + ' [mm]<br>')
			s.wfile.write(bytes(out, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a><br><br>', 'utf-8'))

			# try:
			gearBox_photo_path = FusekiRequest.get_gear_box(radius_list)
			# if(gearBox_photo_path != "-1"):
			print("photo_path:", '<img src="'+gearBox_photo_path+'" alt= "Photo missing...">')
			s.wfile.write(bytes('<img src="'+gearBox_photo_path+'" alt= "Photo missing...">', 'utf-8'))

		else:
			s.wfile.write(bytes(head, 'utf-8'))
			s.wfile.write(bytes("<body><p>The path: " + path + "</p>", "utf-8"))
			s.wfile.write(bytes('</body></html>', "utf-8"))
			
	def do_POST(s):

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		fav = '<link rel="icon" href="favicon_10.ico" type="image/x-icon"/>'
		head = '<html lang="en"> <head> <title> Gearbox </title>'+fav+'</head>'
		
		path = s.path
			
		if path.find("/setRadius") != -1:
			# Get nGears variable
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			nGears = param_line.split("=")[1]

			# HTML title ++
			s.wfile.write(bytes(head, 'utf-8'))
			s.wfile.write(bytes('<section><h1>GearBox - building [2/2]</h1>', 'utf-8'))
			s.wfile.write(bytes('<form action = "/review" method="post">', 'utf-8'))
			s.wfile.write(bytes(nGears + ' gears chosen! Choose the radiuses:<br><br>', 'utf-8'))
			
			# Making a field for each gear radius
			for i in range(int(nGears)): # nGears
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
			nGears = len(pairs)
			for i in range(0, nGears):
				radius_list.append(int(pairs[i].split("=")[1]))

			# Write up the page
			out = head+"""<section><h1>GearBox - review </h1>
					""" + str(nGears) + ' gears chosen. Radiuses are as follows:<br><br>'
			for i in range(nGears):
				out += ('Gear nr.' + str(i) + ': ' + str(radius_list[i]) + ' [mm]<br>')
			s.wfile.write(bytes(out, 'utf-8'))
			s.wfile.write(bytes('<a href="/"><button>Go back</button></a><br><br>', 'utf-8'))

			# Convert list to wanted format			
			string_radius_list = str(radius_list).replace(" ", "")


			try:
				gearBox_photo_path = FusekiRequest.get_photo_path_from_db(string_radius_list)
				if(gearBox_photo_path != "-1"):
					s.wfile.write(bytes('<img src="./Product_images/test.jpg" alt= "Photo missing...">', 'utf-8'))
				else:
					s.wfile.write(bytes('The gearbox was not found in the database. We will supply it when it is ready.', 'utf-8'))
			except:
				s.wfile.write(bytes("Something went wrong", 'utf-8')) #'That gearbox would\'ve been too cool for the program to display it.'

			# Skjema for bestilling
			form = """<form action="/reciept">
                <h2>We're ready to take your order!</h2>
                <fieldset>
                    <legend>Contact information</legend>
                    <label for="company_name">Company name</label><br>
                    <input type="text" name="company_name" placeholder="Company name" id="company_name"><br>
                    <label for="contact_person">Contact person</label><br>
                    <input type="text" name="contact_person" id="contact_person" placeholder="Contact person" pattern="^[a-zA-ZæøåÆØÅ -]+$"><br>
                    <label for="phone">Phone</label><br>
                    <input type="number" name="phone" placeholder="Phone" id="phone"><br>
                    <label for="email">E-mail</label><br>
                    <input class="last" type="email" name="email" placeholder="E-mail" id="email"><br>
                </fieldset>
                <fieldset>
                    <legend>Gear specifications</legend>
                    <label for="material">Material </label><br>
                    <select id= material" name= material">
                        <option value="" disabled selected>Material</option>
                        <option>Brass</option>
                        <option>Steel</option>
                        <option>Diamond</option>
                        <option>Uncertain</option>
                    </select><br>
                    <label for="color">Color</label><br>
                    <select id="color" name="color">
                        <option value="" disabled selected>Color</option>
                        <option>Default</option>
                        <option>Have it painted</option>
                        <option>Uncertain</option>
                    </select><br>
                    <label for="comments">Other comments</label><br>
                    <textarea class="last" name="comments" placeholder="Other comments" id="comments" rows="4" cols="50"></textarea><br>
                </fieldset>
                <input type="submit" value="Order now!" id="submit">
            	</form></section>"""
			s.wfile.write(bytes(form, 'utf-8'))
	
		elif path.find("/reciept") != -1:
			# Get the arguments
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			param_line = post_body.decode()
			pairs = param_line.split("&")
			nGears = len(pairs)
			for i in range(0, nGears):
				radius_list.append(int(pairs[i].split("=")[1]))

			FusekiRequest.add_order()


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

# Valeria