import re
from database.logFunction import LogFunction
from database.databaseFunctions import databaseFunctions
from validation.encrypt import decrypt_message
from validation.encrypt import encrypt_message

class Validation:
    def __init__(self):
        self.logger = LogFunction()
    
    # Behandeld
    def username_validation(self, username, logged_in_user):
        db = databaseFunctions()
        if isinstance(username, str) and 8 <= len(username) <= 12 and re.match(r'^[a-zA-Z_][\w\'.]*$', username) and username not in db.queryAllUsers():
            return True
        print('Username is not valid')
        # oude log
        # self.logger.addLogToDatabase(logged_in_user, encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username that didn't confide by the username format"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=logged_in_user, activity="Incorrect username input", additional_info="Tried inputting a username that didn't confide by the username format", suspicious="No")
        return False
    
    # Behandeld
    def name_validation(self, name, username):
        if name.isalpha() and 1 <= len(name) <= 30:
            return True
        print('Name is not valid')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect name input"), encrypt_message("Tried a non-string input for a name field"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect name input", additional_info="Tried a non-string input for a name field", suspicious="No")
        return False
    
    # Behandeld
    def password_validation(self, password, username):
        if 12 <= len(password) <= 30 and re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,30}$", password):
            return True
        print('Password is not valid')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which did not conform to the password rules"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Unsuccessful password input", additional_info="Tried inputting a password which did not conform to the password rules", suspicious="No")
        return False
    
    # Behandeld
    def password_update_validation(self, password, username):
        if 12 <= len(password) <= 30 and re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,30}$", password):
            return True
        print('Password is not valid')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which did not conform to the password rules"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Unsuccessful password input", additional_info="Tried inputting a password which did not conform to the password rules", suspicious="No")
        return False
    
    # Behandeld
    def username_login_validation(self, username):
        if isinstance(username, str) and re.match(r'^[a-zA-Z_][\w\'.]*$', username):
            return True
        print('Username is not valid')
        # oude log
        # self.logger.addLogToDatabase("", encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username that didn't confide by the username format"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username="", activity="Incorrect username input", additional_info="Tried inputting a username that didn't confide by the username format", suspicious="No")
        return False
    
    # Behandeld
    def password_login_validation(self, password):
        if 12 <= len(password) <= 30 and re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password):
            return True
        print('Password is not valid')
        # oude log
        # self.logger.addLogToDatabase(encrypt_message("unknown user"), encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which did not conform to the password rules"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username="unknown user", activity="Unsuccessful password input", additional_info="Tried inputting a password which did not conform to the password rules", suspicious="No")
        return False

    # Behandeld
    def age_validation(self, age, username):
        """ Leeftijd moet een getal tussen 5 en 110 zijn. """
        if age.isdigit() and 5 <= int(age) <= 110:
            return True
        print('Age input is not correct')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect age input"), encrypt_message("Age was not between 5 and 110"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect age input", additional_info="Age was not between 5 and 110", suspicious="No")
        return False
    
    # Behandeld
    def weight_validation(self, weight, username):
        """ Gewicht moet een getal tussen 20 en 350 zijn. """
        if weight.isdigit() and 20 <= int(weight) <= 350:
            return True
        print('Weight input is not correct')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect weight input"), encrypt_message("Weight was not between 20 and 350"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect weight input", additional_info="Weight was not between 20 and 350", suspicious="No")
        return False
    
    # Behandeld
    def streetname_validation(self, streetname, username):
        if isinstance(streetname, str):
            return True
        print('Streetname input is not correct')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect streetname input"), encrypt_message("Tried a non-string input for a streetname"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect streetname input", additional_info="Tried a non-string input for a streetname", suspicious="No")
        return False
                                     
    # Behandeld
    def housenumber_validation(self, housenumber, username):
        if housenumber.isdigit() and re.match(r"^[1-9]\d*(?:[ -]?(?:[a-zA-Z]+|[1-9]\d*))?$", housenumber):
            return True
        print('House number input is not correct')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect housenumber input"), encrypt_message("Tried a housenumber that didn't confide to housenumber format"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect housenumber input", additional_info="Tried a housenumber that didn't confide to housenumber format", suspicious="No")
        return False

    # Behandeld
    def zipcode_validation(self, zipcode, username):
        if re.match(r"^[1-9][0-9]{3} ?(?!sa|sd|ss)[a-zA-Z]{2}$", zipcode):
            return True
        print('Zipcode is not valid')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect zipcode input"), encrypt_message("Tried a zipcode that didn't confide to the zipcode format"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect zipcode input", additional_info="Tried a zipcode that didn't confide to the zipcode format", suspicious="No")
        return False
    
    # Behandeld 
    def phone_number_validation(self, number, username):
        if re.match(r"\+31-6-\d{8}", number):
            return True
        print('phone number is not valid')
        print('It should be in the format +31-6-xxxxxxxx')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect phonenumber input"), encrypt_message("Tried a phonenumber that didn't confide to the phonenumber format"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect phonenumber input", additional_info="Tried a phonenumber that didn't confide to the phonenumber format", suspicious="No")
        return False
    
    # Behandeld 
    def email_validation(self, email, username):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        print('email is not valid')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect email input"),encrypt_message("Tried an email input which was not valid"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect email input", additional_info="Tried an email input which was not valid", suspicious="No")
        return False
    
    # Behandeld
    def city_validation(self, city, username):
        list_city = ['Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Maastricht', 'Den Haag', 'Eindhoven', 'Tilburg', 'Breda', 'Arnhem']
        if city.isdigit() and 1 <= int(city) <= 10:
            return True
        print('city input is not correct')
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect city input"), encrypt_message("Tried a city input which was not between 1 and 10"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect city input", additional_info="Tried a city input which was not between 1 and 10", suspicious="No")
        return False
     
    # Behandeld
    def gender_validation(self, gender, username):
        if isinstance(gender, str) and re.match(r"^[FfMm]$", gender):
            return True
        print("Try again, Must be f/F or m/M:")
        # oude log
        # self.logger.addLogToDatabase(username, encrypt_message("Incorrect gender input"), encrypt_message("Tried a non-string input"), encrypt_message("No"))
        # nieuwe log
        self.logger.addLogToDatabase(username=username, activity="Incorrect gender input", additional_info="Tried a non-string input", suspicious="No")
        return False