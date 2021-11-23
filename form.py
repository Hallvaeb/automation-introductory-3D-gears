

class FormCreator(object):
    # Made a class so making multiple versions of the form and switching between is easy,
    # should one want for example separate forms for private or company customers...

    def create_form_private_customer(radius_list):
            # This returns a predefined form
            return """<form action="/reciept" method="post">
                    <h2>We're ready to take your order!</h2>
                    <fieldset>
                        <legend>Contact information</legend>
                        <label for="customer_name">Full name</label><br>
                        <input type="text" name="customer_name" id="customer_name" placeholder="Your name, sir" ><br>
                        <label for="address">Address</label><br>
                        <input type="text" name="address" placeholder=".. For delivery, not visits.." id="address"><br>
                        <label for="phone">Phone</label><br>
                        <input type="number" name="phone" placeholder="Phone" id="phone"><br>
                        <label for="email">E-mail</label><br>
                        <input class="last" type="email" name="email" placeholder="E-mail" id="email" required 
                            oninvalid="this.setCustomValidity('Email req. as it is used as customer key in db')" oninput="this.setCustomValidity('')"><br>
                    </fieldset>
                    <input type="hidden" name="radius_list" value='"""+FormCreator.list_to_string(radius_list)+"""'>
                    <fieldset>
                        <legend>Gear specifications</legend>
                        <label for="material">Material </label><br>
                        <select id= material" name= material">
                            <option value="" disabled selected>Material</option>
                            <option>Brass</option>
                            <option>Steel</option>
                            <option>Diamond</option>
                            <option>Uncertain</option>
                        </select><br>
                        <label for="color">Color</label><br>
                        <select id="color" name="color">
                            <option value="" disabled selected>Color</option>
                            <option>None</option>
                            <option>Have it painted</option>
                            <option>Uncertain</option>
                        </select><br>
                    </fieldset>
                    <input type="submit" value="Order now!" id="submit">
                    </form></section>"""


    def create_form_private_customer_DUMMY(radius_list):
            # This returns a ALREADY VALUED form for faster testing
            form = """<form action="/reciept" method="post">
                    <h2>We're ready to take your order!</h2>
                    <fieldset>
                        <legend>Contact information</legend>
                        <label for="customer_name">Full name</label><br>
                        <input type="text" name="customer_name" id="customer_name" placeholder="Your name, sir" value="Test Lobov" autofocus><br>
                        <label for="address">Address</label><br>
                        <input type="text" name="address" placeholder=".. For delivery, not visits.." id="address" value="Testing street 10"><br>
                        <label for="phone">Phone</label><br>
                        <input type="number" name="phone" placeholder="Phone" id="phone" value="01234567"><br>
                        <label for="email">E-mail</label><br>
                        <input class="last" type="email" name="email" placeholder="E-mail" id="email" required 
                            oninvalid="this.setCustomValidity('Email req. as it is used as customer key in db')" oninput="this.setCustomValidity('')" 
                            value="test_email@gmail.com"><br>
                    </fieldset>
                    <input type="hidden" name="radius_list" value=\""""+FormCreator.list_to_string(radius_list)+"""\">
                    <fieldset>
                        <legend>Gear specifications</legend>
                        <label for="material">Material </label><br>
                        <select id= material" name= material">
                            <option value="" disabled selected>Material</option>
                            <option>Brass</option>
                            <option>Steel</option>
                            <option>Diamond</option>
                            <option>Uncertain</option>
                        </select><br>
                        <label for="color">Color</label><br>
                        <select id="color" name="color">
                            <option value="" disabled selected>Color</option>
                            <option>None</option>
                            <option>Have it painted</option>
                            <option>Uncertain</option>
                        </select><br>
                    </fieldset>
                    <input type="submit" value="Order now!" id="submit">
                    </form></section>"""
            return form
                    

    def list_to_string(radius_list):
        return str(radius_list).replace("%5B", "[").replace("%2C", ",").replace("%5D", "]")