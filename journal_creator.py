

class JournalCreator(object):
    
    def create_gear_box_journal_file(radius_list, gear_box_id):

        try:
            # --------- THIS IS THE PATH TO WHERE THE ---------
            print("CREATE JOURNAL INNE I TRY")
            order_path = "C://Users/Eier/OneDrive/Studier/TMM4270/TMM4270_A3/"
    
            # Read the template file
            f = open(order_path+"/Templates/gearBox_template_imagetaker.py", "r")
            print("CREATE JOURNAL INNE I TRY")

            txt = f.read()
            txt_replaced = txt.replace("<RADIUS_LIST>", str(radius_list)).replace("<PHOTO_NAME>", str(gear_box_id))
            print("CREATE JOURNAL INNE I TRY")
            f.close()
            
            # Write a new temporary file.
            print("CREATE JOURNAL INNE I TRY")
            print(order_path+"Product_orders/gearBox_order_"+ str(gear_box_id) +".py")
            f = open(order_path+"Product_orders/gearBox_order_"+ str(gear_box_id) +".py", "w")
            print("HER?")
            # Replacement section, replace the old gear_radiuses with the ones from the userinput
            f.write(txt_replaced)
            print("HER?")
            print("CREATE JOURNAL INNE I TRY")
            f.close()

            return True

        except:
            return False