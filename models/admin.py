from models.consultant import User
from database.databaseFunctions import databaseFunctions
# admin function iherit from class consultant
# admin class has the following attributes and methods:
# ● To check the list of users and their roles.
# ● To define and add a new consultant to the system.
# ● To modify or update an existing consultant’s account and profile.
# ● To delete an existing consultant’s account.
# ● To reset an existing consultant’s password (a temporary password).
# ● To make a backup of the system and restore a backup (members information and users’ data).
# ● To see the logs file(s) of the system.
# ● To add a new member to the system.
# ● To modify or update the information of a member in the system.
# ● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).
# ● To search and retrieve the information of a member.




class Admin(User):
    def __init__(self, id, first_name, last_name, username, password, registration_date,role = "admin"):
        super().__init__(id, first_name, last_name, username, password, registration_date, role) 
    
    def show_users(self):
        if self.is_authorized("admin"):
            print("Here is the list with all the users in our unique meal:" + "\n")
            db = databaseFunctions()
            db.show_user()
        else:
            print("You are not authorized to view this information" + "\n")
    
    
    def add_consultant(self):
        from validation.inputvalidation import Validation
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            print("Welcome, you can now add a new consultant to the system")
            print("Please enter the following information to add a new consultant to the system" + "\n")
            val = Validation()

            errorCounter = 0

            first_name = input("Please enter the first name of the consultant: ")
            while not val.name_validation(first_name, self.username):
                print("Invalid first name")
                errorCounter += 1
                if errorCounter > 2:
                    print("Too many errors, exiting")
                    return
                first_name = input("Please enter the first name of the consultant: ")

            last_name = input("Please enter the last name of the consultant: ")
            while not val.name_validation(last_name, self.username):
                print("Invalid last name")
                errorCounter += 1
                if errorCounter > 2:
                    print("Too many errors, exiting")
                    return
                last_name = input("Please enter the last name of the consultant: ")

            username = input("Please enter the username of the consultant: ")
            while not val.username_validation(username, self.username):
                print("Invalid username")
                errorCounter += 1
                if errorCounter > 2:
                    print("Too many errors, exiting")
                    return
                username = input("Please enter the username of the consultant: ")

            password = input("Please enter the password of the consultant: ")
            while not val.password_validation(password, self.username):
                print("Invalid password")
                errorCounter += 1
                if errorCounter > 2:
                    print("Too many errors, exiting")
                    return
                password = input("Please enter the password of the consultant: ")

            # print("TESTEN: ", first_name, last_name, username, password)
            if first_name and last_name and username and password:
                adFunc = AdminFunctions()
                adFunc.add_consultant(self, first_name, last_name, username, password)
        else:
            print("You are not authorized to add a new consultant to the system" + "\n")

    def modify_consultant(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now modify the information of a consultant" + "\n")
            adFunc.modify_consultant(self)
        else:
            print("You are not authorized to modify the information of a consultant" + "\n")

    def update_consultant(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now update the information of a consultant" + "\n")
            adFunc.update_consultant(self)
        else:
            print("You are not authorized to update the information of a consultant" + "\n")
    
    def delete_consultant(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now delete a consultant from the system" + "\n")
            adFunc.delete_consultant(self)
        else:
            print("You are not authorized to delete a consultant from the system" + "\n")

    def delete_member(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now delete a member from the system" + "\n")
            adFunc.delete_member(self)
        else:
            print("You are not authorized to delete a member from the system" + "\n")

    def request_temporary_password(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now request a temporary password for a consultant" + "\n")
            adFunc.reset_consultant_password(self)
        else:
            print("You are not authorized to request a temporary password for a consultant" + "\n")

    def view_logs(self):
        from database.logFunction import LogFunction
        if self.is_authorized("admin"):
            logger = LogFunction()
            print("Welcome, you can now view the logs of the system" + "\n")
            logger.getLogs()
        else:
            print("You are not authorized to view the logs of the system" + "\n")

    def create_backup(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("Welcome, you can now create a backup of the system" + "\n")
            adFunc.create_backup()
        else:
            print("You are not authorized to create a backup of the system" + "\n")
    
    def restore_backup(self):
        from database.adminFunctions import AdminFunctions
        if self.is_authorized("admin"):
            adFunc = AdminFunctions()
            print("You have chosen to restore a backup of the system" + "\n")
            print("Please note that restoring a backup will overwrite the current system data" + "\n")
            print("Also note that you will be logged out of the system after restoring the backup" + "\n")
            confirm = input("Do you want to continue? (y/n): ")

            if confirm.lower() == "y":
                adFunc.restore_backup()
                print("Exiting program")
                exit()
            else:
                return
            
            # print("Welcome, you can now restore a backup of the system" + "\n")
        else:
            print("You are not authorized to restore a backup of the system" + "\n")
        

    
    
