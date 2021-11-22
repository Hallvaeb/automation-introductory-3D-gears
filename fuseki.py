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


	def is_customer_in_db(customer_phone):
		# query that ask if customer is in db 
		# retrun 0 if customer in db
		
		QUERY = '''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?customerPhone 
		WHERE {
			?Customer kbe:hasPhone ?customerPhone.
		FILTER ( EXISTS { ?Customer kbe:hasPhone "''' + str(customer_phone) + '''"} )
		}
		'''
		PARAMS = {"query": QUERY}
		r = requests.get(url = URL, params = PARAMS) 
		#print("Result:", r.text)
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 1
		return 0
		
		
		
	def add_customer_to_db(customer_list):
		# INPUT customer_list: [Name, address, phone, email, material, color, radius_list[]]
	 	# return 0 when added
		
		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(customer_list[2]) + ''' a kbe:Customer.
  			kbe:''' + str(customer_list[2]) + ''' kbe:hasName "''' + str(customer_list[0]) + '''".
  			kbe:''' + str(customer_list[2]) + ''' kbe:hasAddress "''' + str(customer_list[1]) + '''".
  			kbe:''' + str(customer_list[2]) + ''' kbe:hasPhone "''' + str(customer_list[2]) + '''".
  			kbe:''' + str(customer_list[2]) + ''' kbe:hasEmail "''' + str(customer_list[3]) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_customer_in_db(customer_list[2])


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
		# INPUT gearBox_list: [gearBox_id, radiusList, photoPath, color, material]
	 	# return 0 when added
		new_gearBox_list = gearBox_list#.replace(" ", "").replace("'", "")

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(new_gearBox_list[0]) + ''' a kbe:GearBox.
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasRadiusList "''' + str(new_gearBox_list[1]) + '''".
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasPhotoPath "''' + str(new_gearBox_list[2]) + '''".
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasColor "''' + str(new_gearBox_list[3]) + '''".
  			kbe:''' + str(new_gearBox_list[0]) + ''' kbe:hasMaterial "''' + str(new_gearBox_list[4]) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_gearBox_in_db(new_gearBox_list[1])

	# def add_order_to_db(hele driten):
		# ID = IDGenerator.get_order_id(gear_id, customer_id)


	# def link_order_costumer(order_list):
	# 	# INPUT: [Name, address, phone, email, material, color, radius_list[]]

	# 	UPDATE = ('''
	# 	PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	# 	INSERT {
  	# 		kbe:''' + str(id.create_order_id(order_list)) + ''' a kbe:Order.
  	# 		kbe:''' + str(id.create_order_id(order_list)) + ''' kbe:hasCustomer "''' + str(id.create_customer_id(order_list)) + '''".
  	# 		kbe:''' + str(id.create_order_id(order_list)) + ''' kbe:hasGearBox "''' + str(id.create_gearbox_id(order_list)) + '''"
	# 	}
	# 	WHERE {
	# 	}
	# 	''')

	# 	PARAMS = {"update": UPDATE}
	# 	r = requests.post(url = URL+"/update", data = PARAMS)

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


print(FusekiHandler.add_customer_to_db(["Frida Frosk", "Dammen", 46666666,"frida@mail.com"]))
print(FusekiHandler.add_gearBox_to_db(["JGsitt", [40,506,700], "liksomlink", "ROSA<3", "Diamant"]))


#  PROBLEM: RadiusList må gies inn som string, ikke list. Fordi list ikke har .replace muligheter.
#  LØSNING: RadiusList gies inn som list, driter i å replace mellomrommene. :)) Må inn i IDGENERATOR og endre litt der.
# MERK: FÅR LOV TIL Å LEGGE TIL FLERE GEARS MED SAMME GEARBOXID, MEN DET BLIR IKKE DUPLIKATER AV DE!


# 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