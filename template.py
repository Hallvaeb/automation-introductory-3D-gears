from datetime import datetime


class TemplateCreator(object):
    
    def make_gear_box_in_NX(radius_list):

        # --------- THIS IS THE PATH TO WHERE THE ---------
        order_path = "C://Users/Eier/OneDrive/Studier/TMM4270/TMM4270_A3/"
 
        orderID = str(datetime.now()).replace(" ", "").replace(".","").replace(":","").replace("-","")
        
        # Read the template file
        f = open(order_path+"/Templates/gearBox_template.py", "r")
        txt = f.read()
        f.close()
        
        # Write a new temporary file.
        f = open(order_path+"/Product_orders/gearBox_temporary"+ orderID +".py", "w")

        # Replacement section, replace the old gear_radiuses with the ones from the userinput
        txt_replaced = txt.replace("<RADIUS_LIST>", str(radius_list))
        f.write(txt_replaced)
        f.close()

    make_gear_box_in_NX([10,20,30])