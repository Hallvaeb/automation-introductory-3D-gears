#fusekiRequest.py

# importing the requests library
import requests 
from nxRequest import nxRequest

#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#

URL = "http://127.0.0.1:3030/kbe"

class FusekiRequest(object):

	def get_photo_path_from_db(string_radius_list):
		PARAMS = {'query':"""
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	SELECT ?photoPath
	WHERE {
		?GearBox kbe:hasPhotoPath ?photoPath.
  		?GearBox kbe:hasRadiusList ?radiusList.
	FILTER (?radiusList =""" + string_radius_list + """) 
		}
		"""}
		# Spørre databasen, dette jobber Johanne på.
		# Gir en photo
		# return photo_path

	@staticmethod
	def get_gear_box(radius_list):
		
		# photo_path = get_photo_path_from_db(radius_list):
		# # if(photo_path == "/no_path"):
		# 	# # Object not found in db
		# 	# photo_path = nxRequest.make_gear_box_in_NX(radius_list)
		# 	return photo_path
		# else():
			# Check if path is a path and return it
			# return photo_path

		print("getGearBox")
		photo_path = nxRequest.make_gear_box_in_NX(radius_list)
		# add_to_fuseki_db(photo_path)
		return photo_path
		

	# sending get request and saving the response as response object 
	r = requests.get(url = URL, params = PARAMS) 

	# Checking the result
	print("Result:", r.text)
	data = r.json()
	print("JSON:", data)
	#Checking the value of the parameter
	#print("Data:", data['results']['bindings'][0]['diameter']['value'])



# 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