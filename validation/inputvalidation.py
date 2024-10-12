import re
from database.logFunction import LogFunction
from database.databaseFunctions import databaseFunctions
from validation.encrypt import decrypt_message
from validation.encrypt import encrypt_message

class Validation:
    
    #To check if input is a correct name
    def username_validation(self, username, logged_in_user):

        logger = LogFunction()

        db = databaseFunctions()
        
        if not isinstance(username, str):
            print('Your input is not correct. Please try again:')
            logger.addLogToDatabase(logged_in_user, encrypt_message("Incorrect username input"), encrypt_message("Tried a numerical input where a string was expected"), encrypt_message("No"))
            # username = input("Type here again:")
            # self.username_validation(username, logged_in_user)
            return False
            
        # Check length (between 8 and 12 characters)
        if not 8 <= len(username) <= 12:
            print('Username is not between 8 and 12 characters')
            logger.addLogToDatabase(logged_in_user, encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username wasn't between 8 or 12 characters long"), encrypt_message("No"))
            # print('Try again: ')
            # username = input()
            # self.username_validation(username, logged_in_user)
            return False

        if not re.match(r'^[a-zA-Z_][\w\'.]*$', username):
            print('Username is not valid')
            logger.addLogToDatabase(logged_in_user, encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username that didn't confide by the username format"), encrypt_message("No"))
            # print('Try again: ')
            # username = input()
            # self.username_validation(username, logged_in_user)
            return False

        resultDecrypted = db.queryAllUsers()

        print("DEBUG")
        print(resultDecrypted)
        print("DEBUG")
        
        if username in resultDecrypted:
            print('Username already exists \nTry again: ')
            logger.addLogToDatabase(logged_in_user, encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username which already exists in the database"), encrypt_message("No"))
            # username = input()
            # self.username_validation(username, logged_in_user)
            return False
        return True
    
    def name_validation(self, name, username):
        logger = LogFunction()
        if not name.isalpha():
            # print("Name must be alphabatic. Please try again:")
            # name = input("Type here again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect name input"), encrypt_message("Tried a non-string input for a name field"), encrypt_message("No"))
            # self.name_validation(name, username)
            return False
        if not 1 <= len(name) <= 30:
            print('name is not between 1 and 30 characters')
            # print('Try again: ')
            logger.addLogToDatabase(username, encrypt_message("Incorrect name input"), encrypt_message("Tried inputting a name which was not between 1 and 30 characters"), encrypt_message("No"))
            # name = input()
            # self.name_validation(name, username)
            return False

        # return name.capitalize()
        return True
    
    def password_validation(self, password, username):
        logger = LogFunction()
        if not 12 <= len(password) <= 30:
            print('password is not between 12 and 30 characters')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull update"), encrypt_message("Tried inputting a password which was not between 12 and 30 characters"), encrypt_message("No"))
            # password = input("Try again:")
            # self.password_validation(password, username)
            return False
        # print("This is a test: " + password)
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,30}$", password):
            print('password did not contain any special characters')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull update"), encrypt_message("Tried inputting a password which did not confide to the password rules"), encrypt_message("No"))
            # password = input("Try again:")
            # self.password_validation(password, username)
            return False
        return True
    
    # HIERONDER STAAT DE OUDE PASSWORD_UPDATE_VALIDATION FUNCTIE
    def password_update_validation(self, password, username):
        logger = LogFunction()
        if not 12 <= len(password) <= 30:
            print('password is not between 12 and 30 characters')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull password update"), encrypt_message("Tried inputting a password which was not between 12 and 30 characters"), encrypt_message("No"))
            password = input("Try again:")
            self.password_validation(password, username)

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password):
            print('password is not valid')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull password update"), encrypt_message("Tried inputting a password which did not confide to the password rules"), encrypt_message("No"))
            password = input("Try again:")
            self.password_validation(password, username)
        return password
    
    # HIERONDER STAAT DE NIEUWE PASSWORD_UPDATE_VALIDATION FUNCTIE
    def password_update_validation(self, password, username):
        logger = LogFunction()
        if not 12 <= len(password) <= 30:
            print('password is not between 12 and 30 characters')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull password update"), encrypt_message("Tried inputting a password which was not between 12 and 30 characters"), encrypt_message("No"))

            return False
        
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password):
            print('password is not valid')
            logger.addLogToDatabase(username, encrypt_message("Unsuccessfull password update"), encrypt_message("Tried inputting a password which did not confide to the password rules"), encrypt_message("No"))

            return False
        return True
   
    #CHECK TO DO

    # # HIERONDER STAAT DE OUDE USERNAME_LOGIN_VALIDATION FUNCTIE
    # def username_login_validation(self, username, attempt=0, max_attempts=3):
    #     logger = LogFunction()
    #     # Check if the input is a string
    #     while attempt < max_attempts:
    #         if not isinstance(username, str):
    #             print('Your input is not correct. Please try again:')
    #             username = input("Type here again:")
    #             logger.addLogToDatabase(username, encrypt_message("Unsuccesfull username login"), encrypt_message("Tried logging in with an incorrect username"), encrypt_message("No"))
    #             attempt += 1
    #             continue
    #         if not re.match(r'^[a-zA-Z_][\w\'.]*$', username):
    #             print('Username is not valid')
    #             logger.addLogToDatabase("", encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username that didn't confide by the username format"), encrypt_message("No"))
    #             print('Try again: ')
    #             attempt += 1
    #             username = input()
    #             continue
    #         return username
    #     logger.addLogToDatabase("", encrypt_message("Unsuccessful username login"), encrypt_message("Failed to input a valid username within 3 attempts"), encrypt_message("Yes"))
    #     print("Try again later")
    #     return None
    
    # HIERONDER STAAT DE nieuwe USERNAME_LOGIN_VALIDATION FUNCTIE
    def username_login_validation(self, username):
        logger = LogFunction()
        if not isinstance(username, str):
            print('Your input is not correct. Please try again:')
            logger.addLogToDatabase("", encrypt_message("Incorrect username input"), encrypt_message("Tried a numerical input where a string was expected"), encrypt_message("No"))
            print('DEBUG: KOMT HIJ IN DEZE FALSE? - username_login_validation')
            return False
        if not re.match(r'^[a-zA-Z_][\w\'.]*$', username):
            print('Username is not valid')
            print('DEBUG: KOMT HIJ IN DEZE FALSE? - username_login_validation')

            logger.addLogToDatabase("", encrypt_message("Incorrect username input"), encrypt_message("Tried inputting a username that didn't confide by the username format"), encrypt_message("No"))
            return False
        print('DEBUG: KOMT HIJ IN DEZE TRUE? - username_login_validation')
        
        return True

        
    # # HIERONDER STAAT DE OUDE PASSWORD_LODING_VALIDATION FUNCTIE
    # def password_login_validation(self, password):
    #     logger = LogFunction()
    #     counter = 0 
    #     while counter < 3:
    #         if not 12 <= len(password) <= 30:
    #             print('Password is not between 12 and 30 characters')
    #             logger.addLogToDatabase("", encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which was not between 12 and 30 characters"), encrypt_message("No"))
    #             password = input("Try again:")
    #             counter += 1
    #             continue

    #         if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password):
    #             print('Password is not valid')
    #             logger.addLogToDatabase("", encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which did not conform to the password rules"), encrypt_message("No"))
    #             password = input("Try again:")
    #             counter += 1
    #             continue

    #         return password
       
    #     logger.addLogToDatabase("", encrypt_message("Unsuccessful password input"), encrypt_message("Failed to input a valid password within 3 attempts"), encrypt_message("Yes"))
    #     return None
    
    
    # HIERONDER STAAT DE nieuwe PASSWORD_LOGIN_VALIDATION FUNCTIE
    def password_login_validation(self, password):
        logger = LogFunction()
        if not 12 <= len(password) <= 30:
            print('Password is not between 12 and 30 characters')
            logger.addLogToDatabase("", encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which was not between 12 and 30 characters"), encrypt_message("No"))
            print('DEBUG: KOMT HIJ IN DEZE FALSE? - password_login_validation')
            
            return False
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", password):
            print('Password is not valid')
            logger.addLogToDatabase("", encrypt_message("Unsuccessful password input"), encrypt_message("Tried inputting a password which did not conform to the password rules"), encrypt_message("No"))
            print('DEBUG: KOMT HIJ IN DEZE FALSE? - password_login_validation')
            
            return False
        print('DEBUG: KOMT HIJ IN DEZE TRUE? - password_login_validation')
        
        return True

    
    def age_validation(self, age, username):
        logger = LogFunction()
        if not age.isnumeric():            
            logger.addLogToDatabase(username, encrypt_message("Incorrect age input"), encrypt_message("Tried a non-numerical input"), encrypt_message("No"))
            # age = input()
            # self.age_validation(age, username)
            return False
        if age.isnumeric():
            if not 5 <= int(age) <= 110:
                print('age input is not correct \nTry again: ')
                logger.addLogToDatabase(username, encrypt_message("Incorrect age input"), encrypt_message("Tried an age input which was not between 5 and 110 years old"), encrypt_message("No"))
                # age = input()
                # self.age_validation(age, username)
                return False
        # return age
        return True

    def weight_validation(self, weight, username):
        logger = LogFunction()
        if not weight.isnumeric():
            # print('Input is not correct. Must be numeric. \n Please try again:')
            # weight = input("Type here again:")
            # self.weight_validation(weight, username)
            logger.addLogToDatabase(username, encrypt_message("Incorrect weight input"), encrypt_message("Tried a non-numerical input"), encrypt_message("No"))
            return False
        if not 20 <= int(weight) <= 350:
            print('Weight is not reasonable, please try again: ')
            # weight = input()
            # self.weight_validation(weight, username)
            logger.addLogToDatabase(username, encrypt_message("Incorrect weight input"), encrypt_message("Tried an weight input which was not reasonable"), encrypt_message("No"))
            return False
        # return weight
        return True
    
    def streetname_validation(self, streetname, username):
        logger = LogFunction()
        if not isinstance(streetname, str):
            # print('streetname is not a string')
            # streetname = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect streetname input"), encrypt_message("Tried a non-string input"), encrypt_message("No"))
            # self.streetname_validation(streetname, username)
            return False
        # return streetname.capitalize()
        return True
    
    def housenumber_validation(self, housenumber, username):
        logger = LogFunction()
        while not housenumber.isnumeric():
            # print('House number is not numeric')
            logger.addLogToDatabase(username, encrypt_message("Incorrect housenumber input"), encrypt_message("Tried a non-numerical input"), encrypt_message("No"))
            # housenumber = input("Try again: ")
            return False

        while not re.match(r"^[1-9]\d*(?:[ -]?(?:[a-zA-Z]+|[1-9]\d*))?$", housenumber):
            print('House number is not valid')
            logger.addLogToDatabase(username, encrypt_message("Incorrect housenumber input"), encrypt_message("Tried a housenumber that didn't confide to housenumber format"), encrypt_message("No"))
            # housenumber = input("Try again: ")
            return False
        # return housenumber
        return True

    def zipcode_validation(self, zipcode, username):
        logger = LogFunction()
        if not re.match(r"^[1-9][0-9]{3} ?(?!sa|sd|ss)[a-zA-Z]{2}$", zipcode):
            # print('Zipcode is not valid')
            # zipcode = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect zipcode input"), encrypt_message("Tried a zipcode that didn't confide to the zipcode format"), encrypt_message("No"))
            # self.zipcode_validation(zipcode, username)
            return False
        # return zipcode
        return True
    
 
    def phonenumber_validation(self, number, username):
        logger = LogFunction()
        if not re.match(r"\+31-6-\d{8}", number):
            print('phone number is not valid')
            print('It should be in the format +31-6-xxxxxxxx')
            number = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect phonenumber input"), encrypt_message("Tried a phonenumber that didn't confide to the phonenumber format"), encrypt_message("No"))
            # self.phonenumber_validation(number, username)
            return False
        # return number
        return True

    def email_validation(self, email, username):
        logger = LogFunction()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print('email is not valid')
            email = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect email input"), encrypt_message("Tried an email input which was not valid"), encrypt_message("No"))
            # self.email_validation(email, username)
            return False
        # return email
        return True
    
    def city_validation(self, city, username):
        logger = LogFunction()
        list_city = ['Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Maastricht', 'Den Haag', 'Eindhoven', 'Tilburg', 'Breda', 'Arnhem']
        if not city.isnumeric():
            print('incorrect input. Choose any of the given cities by inputting a number')
            city = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect city input"), encrypt_message("Tried a non-numeric input"), encrypt_message("No"))
            # self.city_validation(city, username)
            return False
        if not 1 <= int(city) <= 10:
            print('city input was not between 1 and 10')
            # print('city is not numeric')
            city = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect city input"), encrypt_message("Tried a city input which was not between 1 and 10"), encrypt_message("No"))
            # self.city_validation(city, username)
            return False
        # return list_city[int(city)-1]
        return True
    
    def gender_validation(self, gender, username):
        logger = LogFunction()
        if not isinstance(gender, str):

            # gender = input("Try again:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect gender input"), encrypt_message("Tried a non-string input"), encrypt_message("No"))
            # self.gender_validation(gender, username)
            return False
            
        if not re.match(r"^[FfMm]$", gender):

            gender = input("Try again, Must be f/F or m/M:")
            logger.addLogToDatabase(username, encrypt_message("Incorrect gender input"), encrypt_message("Not a valid gender input"), encrypt_message("No"))
            return False
        # return gender.upper()
        return True
        
