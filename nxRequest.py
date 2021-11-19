# from GearTrain import GearTrain

        #--------------Vi oppdaterer radiuslisten i py-filen som skal brukes for å lage GearBoxen i NX:--------------#

class nxRequest():
    
    # OrderNumber for each order
    # def orderNum(): #ellernoe, se på det senere


    def make_gear_box_in_NX(radius_list):
        # Reading the template file
        f = open("C:\\Users\\johagl\\TMM4270_A3\\Templates\\gearBox_template.py", "r")
        txt = f.read()
        print("before:", txt)
        f.close()

        # #Writing a new temporary file
        # f = open("C:\\Users\\johagl\\TMM4270_A3\\Product_orders\\gearBox_temporary"+str(orderNumber)+".py", "w")

        # #Replacement section, replace the old gear_radiuses with the ones from the use input
        # txt_replaced = txt.replace(<RADIUS_LIST>, radius_list)
        # #change it to the new radius 
        # f.write(txt_replaced)
        # f.close()