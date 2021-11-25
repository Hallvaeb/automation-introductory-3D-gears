import requests

from id import IDGenerator 

# TING Å SE PÅ:


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
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 1
		return 0
		
	def add_customer_to_db(order_list):
		# INPUT customer_list: [Name, address, phone, email, material, color, photoPath, radius_list[]]
	 	# return 0 when added
		customer_id = IDGenerator.create_customer_id(order_list)
		order_id = IDGenerator.create_order_id(order_list)


		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(customer_id) + ''' a kbe:Customer.
  			kbe:''' + str(customer_id) + ''' kbe:hasName "''' + str(order_list[0]) + '''".
  			kbe:''' + str(customer_id) + ''' kbe:hasAddress "''' + str(order_list[1]) + '''".
  			kbe:''' + str(customer_id) + ''' kbe:hasPhone "''' + str(order_list[2]) + '''".
  			kbe:''' + str(customer_id) + ''' kbe:hasEmail "''' + str(order_list[3]) + '''".
			kbe:''' + str(customer_id) + ''' kbe:hasOrder "''' + str(order_id) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_customer_in_db(order_list[2])


	def is_gearBox_in_db(radius_list):
		# retrun 0 if gearBox in db
		string_radius_list = str(radius_list)#.replace(" ", "")
		# FOR Å KUNNE SETTE INN VED ADD_-DEF MÅ .REPLACE BORT FORDI NÅR VI SETTER INN
		# EN LISTE BLIR DET AUTOMATISK MELLOMROM MELLOM KOMMA OG TALL. SE PÅ DETTE!
		# ER DET NOE VI KAN TA BORT, VI TOK DET VEL MED FOR Å MINIMALISERE ROM FOR FEIL?
		#print(string_radius_list)
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
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 1
		return 0

	def add_gearBox_to_db(order_list):
		# order_list: [Name, address, phone, email, material, color, photoPath, radius_list[]]
	 	# return 0 when added
		gearBox_id  = IDGenerator.create_gearbox_id(order_list)

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(gearBox_id) + ''' a kbe:GearBox.
  			kbe:''' + str(gearBox_id) + ''' kbe:hasRadiusList "''' + str(order_list[-1]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasPhotoPath "''' + str(order_list[-2]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasColor "''' + str(order_list[-3]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasMaterial "''' + str(order_list[-4]) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_gearBox_in_db(order_list[-1])


	# def is_order_in_db(order_list):
	# 	# query that ask if customer is in db 
	# 	# retrun 0 if customer in db
		
	# 	QUERY = '''
	# 	PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	# 	SELECT ?order 
	# 	WHERE {
	# 		?Order kbe:hasPhone ?customerPhone.
	# 		# HER MÅ DET VEL INN BÅDE GearBox_ID OG Customer_ID???
	# 	FILTER ( EXISTS { ?Customer kbe:hasPhone "''' + str(customer_phone) + '''"} )
	# 	}
	# 	'''
	# 	PARAMS = {"query": QUERY}
	# 	r = requests.get(url = URL, params = PARAMS) 
	# 	data = r.json()
		
	# 	if (len(data['results']['bindings']) == 0 ):
	# 		return 1
	# 	return 0

	def add_order_to_db(order_list): #UFERDIG?
		# order_list: [Name, address, phone, email, material, color, photoPath, radius_list[]]
	 	# return 0 when added
		order_id = IDGenerator.create_order_id(order_list)
		customer_id = IDGenerator.create_customer_id(order_list)
		gearBox_id = IDGenerator.create_gearbox_id(order_list)

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(order_id) + ''' a kbe:Order.
  			kbe:''' + str(order_id) + ''' kbe:hasCustomer "''' + str(customer_id) + '''".
  			kbe:''' + str(order_id) + ''' kbe:hasGearBox "''' + str(gearBox_id) + '''".
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_order_in_db()


	# def is_order_customer_linked(order_list): #UFERDIG
	# 	# INPUT: [Name, address, phone, email, material, color, photoPath, radius_list[]]
	# 	order_id = IDGenerator.create_order_id(order_list)
	# 	customer_id = IDGenerator.create_customer_id(order_list)

	# 	# if link is made, return 0
	# 	QUERY = '''
	# 	PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	# 	SELECT ?order 
	# 	WHERE {
  	# 		?Customer kbe:hasOrder ?order.
	# 	FILTER ( EXISTS { ?Customer kbe:hasOrder "''' + str(order_id) + '''"} )
	# 	}
	# 	'''
	# 	PARAMS = {"query": QUERY}
	# 	r = requests.get(url = URL, params = PARAMS) 
	# 	data = r.json()
		
	# 	if (len(data['results']['bindings']) == 0 ):
	# 		return 1
		
	# 	QUERY = '''
	# 	PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	# 	SELECT ?customer 
	# 	WHERE {
  	# 		?Order kbe:hasCustomer ?customer.
	# 	FILTER ( EXISTS { ?Order kbe:hasCustomer "''' + str(customer_id) + '''"} )
	# 	}
	# 	'''
	# 	PARAMS = {"query": QUERY}
	# 	r = requests.get(url = URL, params = PARAMS) 
	# 	data = r.json()
		
	# 	if (len(data['results']['bindings']) == 0 ):
	# 		return 1
	# 	return 0


	# def is_order_gearBox_linked(order_list): #UFERDIG
	# 	# INPUT: [Name, address, phone, email, material, color, photoPath, radius_list[]]
	# 	order_id = IDGenerator.create_order_id(order_list)
	# 	gearBox_id = IDGenerator.create_gearbox_id(order_list)

	# 	#if link is made, return 0
	# 	QUERY = '''
	# 	PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
	# 	SELECT ?gearBox 
	# 	WHERE {
  	# 		?Order kbe:hasGearBox ?gearBox.
	# 	FILTER ( EXISTS { ?Order kbe:hasGearBox "''' + str(gearBox_id) + '''"} )
	# 	}
	# 	'''
	# 	PARAMS = {"query": QUERY}
	# 	r = requests.get(url = URL, params = PARAMS) 
	# 	data = r.json()
		
	# 	if (len(data['results']['bindings']) == 0 ):
	# 		return 1
	# 	return 0
	

	def create_order(order_list): #UFERDIG
		#Input: [customer name, adress, phone, email, radius_list[]] 
		if (FusekiHandler.is_customer_in_db(order_list) == 1): #=1 if customer not i db. then add.
			FusekiHandler.add_customer_to_db(order_list)

		if (FusekiHandler.is_gearBox_in_db(order_list) == 1):  #=1 if gearBox not i db. then add.
			FusekiHandler.add_gearBox_to_db(order_list)
	
		
		# make order object with the customer and gearbox in db : add_order_in_db
		# call templet_file_creator to make the order python-file with the new name


		# link Order with Customer, link Customer with Order.
		# link Order with GearBox.

		# return 0 if order is added to db (if something else, something went wrong)


# INPUT: order_list: [Name, address, phone, email, material, color, photoPath, radius_list[]]
order_list = ["Anine", "Aninegata", 11114111, "anine@mail.com", "Brass", "None", "photoPath[50,60,70,80]", [50,60,70,80]]

print(FusekiHandler.add_gearBox_to_db(order_list))
print(FusekiHandler.add_customer_to_db(order_list))


#  PROBLEM: RadiusList må gies inn som string, ikke list. Fordi list ikke har .replace muligheter.
#  LØSNING: RadiusList gies inn som list, driter i å replace mellomrommene. :)) Må inn i IDGENERATOR og endre litt der.
# MERK: FÅR LOV TIL Å LEGGE TIL FLERE GEARS MED SAMME GEARBOXID, MEN DET BLIR IKKE DUPLIKATER AV DE!


# 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