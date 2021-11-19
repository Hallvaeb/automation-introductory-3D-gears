from datetime import datetime

        #--------------Vi oppdaterer radiuslisten i py-filen som skal brukes for å lage GearBoxen i NX:--------------#

class nxRequest(object):
    
    def make_gear_box_in_NX(radius_list):
        orderID = str(datetime.now()).replace(" ", "").replace(".","").replace(":","").replace("-","")
        # Reading the template file

        f = open("C:\\Users\\Johanne\\TMM4270_A3\\Templates\\gearBox_template.py", "r")
        txt = f.read()
        print("before:", txt)
        f.close()
        
        #Writing a new temporary file.
        f = open("C:\\Users\\Johanne\\TMM4270_A3\\Product_orders\\gearBox_temporary"+ orderID +".py", "w")

        #Replacement section, replace the old gear_radiuses with the ones from the userinput
        txt_replaced = txt.replace("<RADIUS_LIST>", str(radius_list))
        f.write(txt_replaced)
        print("after:", txt_replaced)
        f.close()

    print(make_gear_box_in_NX([10,20,30]))