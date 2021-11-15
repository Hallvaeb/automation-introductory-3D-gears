#fusekiRequest.py

# importing the requests library
import requests 

#--------------Vi spør Fuseki-serveren vha requests om etterspurt brukerinput/radiuskombinasjon finnes i databasen--------------#


URL = "http://127.0.0.1:3030/kbe"
  
# defining a query params  --- DENNE MÅ ENDRES!!!!!!!!!!!
PARAMS = {'query':"""
PREFIX kbe:<http://www.my-kbe.com/shapes.owl#>
SELECT ?gear ?diameter
WHERE {
?gear kbe:hasDiameter ?diameter.
FILTER (?diameter>50) 
}
"""} 
 
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 

# Checking the result
print("Result:", r.text)
data = r.json()
print("JSON:", data)
#Checking the value of the parameter
#print("Data:", data['results']['bindings'][0]['diameter']['value'])

#--------------Vi oppdaterer radiusene i py-filen som skal brukes for å lage GearBoxen i NX:--------------#

# Reading the template file
f = open("C:\\Users\\johagl\\auto\\templates\\gearBox_temp.py", "r")
txt = f.read()
print("before:", txt)

#Writing to the correct location
f = open("C:\\Users\\johagl\\auto\\templates\\gearBox_temp.py", "w")

for i in range(\\BRUKERINPUT//): #ENDRES!!!!!!!!!
	#Replacement section, replace the old gear_radiuses with the ones from the use input
	txt = txt.replace(gear_radius_list[i], radius_list[i])
	#change it to the new radius 
	f.write(txt)

f.close()
