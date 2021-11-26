import requests
from id import IDGenerator 

# TING Å SE PÅ:


#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#

URL = "http://127.0.0.1:3030/kbe"


class FusekiHandler(object):

	def get_photo_name_from_db(radius_list):
		# Convert list to string format			
		string_radius_list = str(radius_list)#.replace(" ", "")

		QUERY = '''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?photoname
		WHERE {
			?GearBox kbe:hasPhotoName ?photoname.
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
		#print("Data:", data['results']['bindings'][0]['photoname']['value'])	
		try:
			# return the n of the photo of this gearbox
			photo_name = data['results']['bindings'][0]['photoname']['value']
			if len(photo_name) == 0:
				return ""
			return photo_name
		except:
			return 0


	def is_customer_in_db(customer_phone):
		# query that ask if customer is in db 
		# retrun 1 (true) if customer in db
		
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
			return 0
		return 1
		
	def add_customer_to_db(order_list):
		# INPUT customer_list: [Name, address, phone, email, material, color, photoname, radius_list[]]
	 	# return 1 (true) when added
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
		# retrun 1 (true) if gearBox in db
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
			return 0
		return 1

	def add_gearBox_to_db(order_list):
		# order_list: [Name, address, phone, email, material, color, photoname, radius_list[]]
	 	# return 1 when added
		gearBox_id  = IDGenerator.create_gearbox_id(order_list)

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(gearBox_id) + ''' a kbe:GearBox.
  			kbe:''' + str(gearBox_id) + ''' kbe:hasRadiusList "''' + str(order_list[-1]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasPhotoName "''' + str(order_list[-2]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasColor "''' + str(order_list[-3]) + '''".
  			kbe:''' + str(gearBox_id) + ''' kbe:hasMaterial "''' + str(order_list[-4]) + '''"
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_gearBox_in_db(order_list[-1])

	def add_gearBox_to_db_rad(gearBox_radius_list):
		# gearBox_list: radius_list[]
	 	# return 1 when added
		gearBox_id  = IDGenerator.create_gearbox_id(gearBox_radius_list)

		UPDATE = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		INSERT {
  			kbe:''' + str(gearBox_id) + ''' a kbe:GearBox.
  			kbe:''' + str(gearBox_id) + ''' kbe:hasRadiusList "''' + str(gearBox_radius_list) + '''".
		}
		WHERE {
		}
		''')

		PARAMS = {"update": UPDATE}
		r = requests.post(url = URL+"/update", data = PARAMS) 
		
		return FusekiHandler.is_gearBox_in_db(gearBox_radius_list)


	def is_order_in_db(order_list):
		# query that ask if customer is in db 
		# retrun 1 if customer in db
		order_id = IDGenerator.create_order_id(order_list)
		customer_id = IDGenerator.create_customer_id(order_list)

		QUERY = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT ?order
		WHERE {
			?Customer kbe:hasOrder ?order.
    		?Order kbe:hasCustomer ?customer.
		FILTER ( 
    		EXISTS { ?Customer kbe:hasOrder "'''+ str(order_id) +'''"} &&
			EXISTS { ?Order kbe:hasCustomer "''' + str(customer_id) + '''" }
  		)}
		''')

		PARAMS = {"query": QUERY}
		r = requests.get(url = URL, params = PARAMS) 
		data = r.json()
		
		if (len(data['results']['bindings']) == 0 ):
			return 0 #FALSE
		return 1

	def add_order_to_db(order_list): #UFERDIG?
		# order_list: [Name, address, phone, email, material, color, photoname, radius_list[]]
	 	# return 1 when added
		order_id = IDGenerator.create_order_id(order_list)
		customer_id = IDGenerator.create_customer_id(order_list)
		gearBox_id = IDGenerator.create_gearbox_id(order_list)
		# print(order_id)
		# print(customer_id)
		# print(gearBox_id)
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
		
		return FusekiHandler.is_order_in_db(order_list)

	def add_photo_name_to_gearbox(radius_list, photo_name): #photo_name = gearbox_id fra id-fil?
		try:
			UPDATE = ('''
			PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
			DELETE { ?GearBox kbe:hasPhotoName ""}
			INSERT { ?GearBox kbe:hasPhotoName "''' + str(photo_name) + '''". }
			WHERE { ?GearBox kbe:hasRadiusList "'''+str(radius_list)+'''" }
			''')
			PARAMS = {"update": UPDATE}
			r = requests.post(url = URL+"/update", data = PARAMS) 
			return 1
		except:
			return 0


	def count_customer_orders(order_list):
		customer_id = IDGenerator.create_customer_id(order_list)	

		QUERY = ('''
		PREFIX kbe:<http://www.my-kbe.com/kbe-system.owl#>
		SELECT (count(?customer) as ?orderCount)
		WHERE {
			?Order kbe:hasCustomer ?customer.
  		FILTER( EXISTS {?Order kbe:hasCustomer "'''+str(customer_id)+'''"} )
		} 
		GROUP BY ?customer
		''')

		PARAMS = {"query": QUERY}
		r = requests.get(url = URL, params = PARAMS) 
		data = r.json()
		try:
			if(len(data['results']['bindings']) == 0):
				return 0
			return int(data['results']['bindings'][0]['orderCount']['value'])+1
		except Exception as e:
			print("fuseki error:", e)



	def create_order(order_list):
		order_id = IDGenerator.create_order_id(order_list)

		if (FusekiHandler.is_customer_in_db(order_list) == 0): #=0(false) if customer not i db. then add.
			c = FusekiHandler.add_customer_to_db(order_list)

		if (FusekiHandler.is_gearBox_in_db(order_list) == 0):  #=0(false) if gearBox not i db. then add.
			c += FusekiHandler.add_gearBox_to_db(order_list)

		c += FusekiHandler.add_order_to_db(order_list)

		if (c == 3):
			return 1
		return 0
		# return 1 if order is added to db (if something else, something went wrong)


# INPUT: order_list: [Name, address, phone, email, material, color, photoname, radius_list[]]
# order_list = ["Åge Stormo", "Slottet", 44332211, "åge@mail.com", "Diamond", "None", "", [10,50,100]]
# order_list_2 = ["Lars", "Gløs", 56565656, "lars@mail.com", "Diamond", "None", "", [58,58,58]]
# order_list_2b = ["Lars", "Gløs", 56565656, "lars@mail.com", "Diamond", "None", "", [58,58,58,58]]

# order_list_3 = ["Jens", "Dragvoll", 121212, "jens@mail.com", "Diamond", "None", "jensPåDrag", [12,12,12]]
# order_list_4 = ["Richard", "Muren", 434343, "richard@mail.com", "Diamond", "None", "richardPåMuren", [43,43,43]]
# order_list_6 = ["Helena", "Oslo", 43542633, "helena@mail.com", "Diamond", "None", "", [44,44]]

# print(FusekiHandler.create_order(order_list))
# print(FusekiHandler.create_order(order_list_2))
# print(FusekiHandler.create_order(order_list_2b))
# print(FusekiHandler.create_order(order_list_3))
# print(FusekiHandler.create_order(order_list_4))
# print(FusekiHandler.create_order(order_list_6))
# print(FusekiHandler.is_order_in_db(order_list_6))




#  PROBLEM: RadiusList må gies inn som string, ikke list. Fordi list ikke har .replace muligheter.
#  LØSNING: RadiusList gies inn som list, driter i å replace mellomrommene. :)) Må inn i IDGENERATOR og endre litt der.
# MERK: FÅR LOV TIL Å LEGGE TIL FLERE GEARS MED SAMME GEARBOXID, MEN DET BLIR IKKE DUPLIKATER AV DE!