

class JournalCreator(object):
    
    def create_gear_box_journal_file(radius_list, gear_box_id):

        try:
            # --------- THIS IS THE PATH TO WHERE THE ---------
            order_path = "C://Users/Eier/OneDrive/Studier/TMM4270/TMM4270_A3/"
    
            # Read the template file
            f = open(order_path+"/Templates/gearBox_template_imagetaker.py", "r")
            txt = f.read()
            txt_replaced = txt.replace("<RADIUS_LIST>", str(radius_list)).replace("<PHOTO_NAME>", str(gear_box_id))
            f.close()
            
            # Write a new temporary file.
            f = open(order_path+"/Product_orders/gearBox_order_"+ str(gear_box_id) +".py", "w")

            # Replacement section, replace the old gear_radiuses with the ones from the userinput
            f.write(txt_replaced)
            f.close()

            return True

        except:
            return False