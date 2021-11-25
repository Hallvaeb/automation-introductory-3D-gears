

class IDGenerator():
    """
        Makes unique IDs for 
        Customer
        Gearbox
        Order
    """
    # [Name, address, phone, email, material, color, photoPath, radius_list[]] #Lagt til photoPath som nest sist.
    # fil = form input list
    def create_customer_id(fil):
        phone = fil[2]
        return phone

    def create_gearbox_id(fil):
        radius_list = fil[-1]
        str_list = "r_" + str(radius_list).replace(", ", "_").replace("[","").replace("]","") +"_" #endret litt
        return str_list

    def create_order_id(fil):
        gearbox_id = str(IDGenerator.create_gearbox_id(fil))
        customer_id = str(IDGenerator.create_customer_id(fil))
        mat = str(IDGenerator.get_material_number(fil[4]))
        col = str(IDGenerator.get_color_number(fil))
        order_id = gearbox_id + customer_id + mat + col 
        return order_id
       

    def create_all_ids(fil):
        """
        """
        gearbox_id = IDGenerator.create_gearbox_id(fil) 
        customer_id = IDGenerator.create_customer_id(fil)
        order_id = IDGenerator.create_order_id(fil)
        return gearbox_id, customer_id, order_id

    def get_material_number(material):
        material_number = {
            "Brass": 1,
            "Steel": 2,
            "Diamond": 3,
            "Uncertain": 4
        }
        return material_number.get(material, 0)

    def get_color_number(fil):
        color = fil[5]
        color_number = {
            "None": 1,
            "Have it painted": 2,
            "Uncertain": 3
        }
        return color_number.get(color, 0)