from models.admin import Admin
from database.superAdminFunctions import SuperAdminFunctions
from validation.inputvalidation import Validation

class SuperAdmin(Admin):
    def __init__(self, id, first_name, last_name, username, password, registration_date):
        super().__init__(id,first_name, last_name, username, password, registration_date, "superadmin")
        
        #TODO: add the following function to the superadmin class
        
        #the following function should be added to the superadmin class
        # def add_admin(self):
        # def modify_admin(self):
        # def delete_admin(self):
        # def request_temporary_admin_password(self):

    def __str__(self):
        return f"superadmin({self.id}, {self.first_name})"

    def __repr__(self):
        return str(self)
    
    def add_admin(self):
        val = Validation()
        superAdFunc = SuperAdminFunctions()

        errorCounter = 0

        if self.is_authorized("superadmin"):
            print("Welcome, you can now add a new admin to the system" + "\n")
            print("Please enter the following information to add a new admin to the system" + "\n")
            
            first_name = input("Please enter the first name of the admin: ")
            while not val.name_validation(first_name, self.username):
                print("Invalid first name")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many failed attempts. Returning to main menu")
                    return
                first_name = input("Please enter the first name of the admin: ")
            
            last_name = input("Please enter the last name of the admin: ")
            while not val.name_validation(last_name, self.username):
                print("Invalid last name")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many failed attempts. Returning to main menu")
                    return
                last_name = input("Please enter the last name of the admin: ")
                # return
            
            username = input("Please enter the username of the admin: ")
            while not val.username_validation(username, self.username):
                print("Invalid username")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many failed attempts. Returning to main menu")
                    return
                username = input("Please enter the username of the admin: ")
            
            password = input("Please enter the password of the admin: ")
            while not val.password_validation(password, self.username):
                print("Invalid password")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many failed attempts. Returning to main menu")
                    return
                password = input("Please enter the password of the admin: ")
                
            superAdFunc.add_Admin(self, first_name, last_name, username, password)
        else:
            print("You are not authorized to add a new admin to the system")
            
    def modify_admin(self):
        superAdFunc = SuperAdminFunctions()
        if self.is_authorized("superadmin"):
            print("Welcome, you can now modify the information of a consultant" + "\n")
            superAdFunc.modify_admin(self)
        else:
            print("You are not authorized to modify the information of a consultant")
        

    def delete_admin(self):
        superAdFunc = SuperAdminFunctions()
        if self.is_authorized("superadmin"):            
            print("Welcome, you can now delete a consultant from the system" + "\n")
            superAdFunc.delete_admin(self)
        else:
            print("You are not authorized to delete a consultant from the system")

    def request_temporary_admin_password(self):
        if self.is_authorized("superadmin"):
            superAdFunc = SuperAdminFunctions()
            print("Welcome, you can now request a temporary password for an admin" + "\n")
            superAdFunc.request_temporary_admin_password(self)
        else:
            print("You are not authorized to request a temporary password for a consultant")