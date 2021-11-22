import requests 

#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#

URL = "http://127.0.0.1:3030/kbe"


class FusekiHandler(object):

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


	def is_customer_in_db(customer_email):
		# query that ask if customer is in db 
		# retrun 0 if customer in db
		
		QUERY = '''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?customerEmail 
		WHERE {
			?Customer kbe:hasEmail ?customerEmail.
		FILTER ( EXISTS { ?Customer kbe:hasEmail "''' + customer_email + '''"} )
		}
		'''
		PARAMS = {"query": QUERY}
		r = requests.get(url = URL, params = PARAMS) 
		#print("Result:", r.text)
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 1
		return 0

	# def add_customer_to_db():
		# EMAIL is unique ID
	# 	# return 0


	def is_gearBox_in_db(radius_list):
		# retrun 0 if gearBox in db
		string_radius_list = str(radius_list)#.replace(" ", "")
		# FOR Å KUNNE SETTE INN VED ADD_-DEF MÅ .REPLACE BORT FORDI NÅR VI SETTER INN
		# EN LISTE BLIR DET AUTOMATISK MELLOMROM MELLOM KOMMA OG TALL. SE PÅ DETTE!
		# ER DET NOE VI KAN TA BORT, VI TOK DET VEL MED FOR Å MINIMALISERE ROM FOR FEIL?
		
		QUERY = '''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?radiusList 
		WHERE {
			?GearBox kbe:hasRadiusList ?radiusList.
		FILTER ( EXISTS { ?GearBox kbe:hasRadiusList "''' + string_radius_list + '''"} )
		}
		'''
		PARAMS = {"query": QUERY}
		r = requests.get(url = URL, params = PARAMS) 
		#print("Result:", r.text)
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 1
		return 0
	

	def add_gearBox_to_db(gearBox_list):
		# INPUT gearBox_list: [gearBoxID, radiusList, photoPath]
	 	# return 0 when added
		new_gearBox_list = gearBox_list#.replace(" ", "").replace("'", "")

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(new_gearBox_list[0]) + ''' a kbe:GearBox.
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasRadiusList "''' + str(new_gearBox_list[1]) + '''".
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasPhotoPath "''' + str(new_gearBox_list[2]) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_gearBox_in_db(new_gearBox_list[1])

	# def add_order_to_db(hele driten):
		# ID = IDGenerator.get_order_id(gear_id, customer_id)


	# def link_order_costumer()

	# def link_order_gearBox():

	
	# def create_order(order_list): 
	# 	#Input: [customer name, adress, phone, email, radius_list[]] 
	# 	if (!is_customer_in_db()): 
	# 		add_customer_to_db()
	# 	# check if customer is in db
	# 	# if true, nothing.
	# 	# if false, call add_customer_to_db

	# 	if (!is_gearBox_in_db()): 
	# 		add_gearBox_to_db()
	# 	# check if gearBox is in db
	# 	# if true, nothing.
	# 	# if false, call add_gearBox_to_db
		
	# 	# make order object with the customer and gearbox in db
	# 	# call templet_file_creator to make the order python-file with the new name


	# 	# link Order with Customer, link Customer with Order.
	# 	# link Order with GearBox.

	# 	# return 0 if order is added to db (if something else, something went wrong)


# Testing what the photo path is
print(FusekiHandler.add_gearBox_to_db(["HallvardssGear",["tall"],"HallvardsGearPath"]))
#  PROBLEM: RadiusList må gies inn som string, ikke list. Fordi list ikke har .replace muligheter.
# MERK: FÅR LOV TIL Å LEGGE TIL FLERE GEARS MED SAMME GEARBOXID, MEN DET BLIR IKKE DUPLIKATER AV DE!


# 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