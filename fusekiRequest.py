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

	def add_order_to_db(order_list): #Input: [company name, contact, phone, email, material, color, comments, radius_list[]]
		#checks if customer and/or gearBox already is in the database. If so,
		# 0 ingen lagt til, fordi begge var der fra før 
		#
		
		
		FusekiRequest.add_customer_to_db(order_list)
		FusekiRequest.add_gearBox_to_db(order_list)

	# def add_customer_to_db():
	# 	#return true NÅR customer er lagt til 

	# def add_gearBox_to_db():
	# 	#return true NÅR gearBox er lagt til



# Testing what the photo path is
#print(FusekiRequest.get_photo_path_from_db("[20,30,40]"))
		




# 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