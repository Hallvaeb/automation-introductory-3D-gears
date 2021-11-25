import os

from fuseki import FusekiHandler


class JournalCreator(object):
    
    def create_gear_box_journal_file(radius_list, photo_name):

        try:
            project_folder_path = str(os.getcwd()).replace(os.sep, "/")

            # Read the template file
            f = open("./Templates/gearBox_template_imagetaker.py", "r")
            txt = f.read()
            txt_replaced = txt.replace("<RADIUS_LIST>", str(radius_list))
            txt_replaced = txt_replaced.replace("<PHOTO_NAME>", str(photo_name))
            txt_replaced = txt_replaced.replace("<PROJECT_FOLDER_PATH>", project_folder_path)
            f.close()
            
            # Write a new temporary file.
            f = open("./Product_orders/gearBox_order_"+ str(photo_name) +".py", "w")
            f.write(txt_replaced)
            f.close()
            FusekiHandler.add_photo_name_to_gearbox(radius_list, photo_name)
            return 1

        except:
            print("Noe gikk feil i gear box journal creator")
            return 0

