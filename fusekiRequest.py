#fusekiRequest.py

# importing the requests library
import requests 
from nxRequest import nxRequest

#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#


URL = "http://127.0.0.1:3030/kbe"

class FusekiRequest(object):

	def get_photo_path_from_db(radius_list):
		PARAMS = {'query':"""
		PREFIX kbe:<http://www.my-kbe.com/shapes.owl#>
		SELECT ?gear ?diameter
		WHERE {
		?gear kbe:hasDiameter ?diameter.
		FILTER (?"""+
		str(radius_list[i]*2)+
		""">50) 
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
		






	# # sending get request and saving the response as response object 
	# r = requests.get(url = URL, params = PARAMS) 

	# # Checking the result
	# print("Result:", r.text)
	# data = r.json()
	# print("JSON:", data)
	# #Checking the value of the parameter
	# #print("Data:", data['results']['bindings'][0]['diameter']['value'])

	# #--------------Vi oppdaterer radiusene i py-filen som skal brukes for å lage GearBoxen i NX:--------------#

	# # Reading the template file
	# f = open("C:\\Users\\johagl\\auto\\templates\\gearBox_template.py", "r")
	# txt = f.read()
	# f.close()

	# print("before:", txt)

	# #Writing a new temporary file
	# f = open("C:\\Users\\johagl\\auto\\templates\\gearBox_temporary"+str(orderNumber)+".py", "w")

	# for i in range(\\BRUKERINPUT//): #ENDRES!!!!!!!!!
	# 	#Replacement section, replace the old gear_radiuses with the ones from the use input
	# 	txt = txt.replace(gear_radius_list[i], radius_list[i])
	# 	#change it to the new radius 
	# 	f.write(txt)
	# f.close()
