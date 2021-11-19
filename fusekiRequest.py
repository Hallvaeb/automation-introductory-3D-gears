#fusekiRequest.py

# importing the requests library
import requests 
from nxRequest import nxRequest

#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#

URL = "http://127.0.0.1:3030/kbe"

class FusekiRequest(object):

	def get_photo_path_from_db(radius_list):
		# Convert list to string format			
		string_radius_list = str(radius_list).replace(" ", "")

		QUERY = '''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?photoPath
		WHERE {
			?GearBox kbe:hasPhotoPath ?photoPath.
			?GearBox kbe:hasRadiusList ?radiusList
		FILTER (?radiusList = "''' + string_radius_list + '''") 
		}
		'''
		PARAMS = {"query": QUERY}
		# Sending get request and saving the response as response object 
		r = requests.get(url = URL, params = PARAMS) 

		# Checking the result
		#print("Result:", r.text)
		data = r.json()
		#print("JSON:", data)
		
		# Checking the value of the parameter
		#print("Data:", data['results']['bindings'][0]['photoPath']['value'])	
		
		# return the photopath of the photo of this gearbox
		photo_path = data['results']['bindings'][0]['photoPath']['value']

		# Validate photo path

		return photo_path


	def is_customer_in_db():
		# query that ask if customer is in db 
		# retrun true if costumer in db

	def add_customer_to_db():
		# return 0


	def is_gearBox_in_db():
		# retrun true if gearBox in db
		
	def add_gearBox_to_db():
		# return 0


	def add_order_to_db():

	def link_order_costumer()

	def link_order_gearBox():

	
	def create_order(order_list): 
		#Input: [customer name, adress, phone, email, radius_list[]] 
		if (!is_customer_in_db()): 
			add_customer_to_db()
		# check if customer is in db
		# if true, nothing.
		# if false, call add_customer_to_db

		if (!is_gearBox_in_db()): 
			add_gearBox_to_db()
		# check if gearBox is in db
		# if true, nothing.
		# if false, call add_gearBox_to_db
		
		# make order object with the customer and gearbox in db
		# call templet_file_creator to make the order python-file with the new name


		# link Order with Customer, link Customer with Order.
		# link Order with GearBox.

		# return 0 if order is added to db (if something else, something went wrong)


# Testing what the photo path is
#print(FusekiRequest.get_photo_path_from_db("[20,30,40]"))
		




# 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