from database.databaseFunctions import databaseFunctions
from validation.inputvalidation import Validation
from database.memberFunctions import MemberFunctions
from tabulate import tabulate

class User:
    def __init__(self, id, first_name, last_name, username, password, registration_date, role):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.registration_date = registration_date
        self.role = role

    def __str__(self):
        return f"{self.id} {self.first_name} {self.last_name} {self.username} {self.registration_date}"
    
    def is_authorized(self, required_role):
        roles_hierarchy = {"consultant": 1, "admin": 2, "superadmin": 3}
        return roles_hierarchy[self.role] >= roles_hierarchy[required_role]
    
    def add_member(self):
        if self.is_authorized("consultant"):
            memFuncs = MemberFunctions()

            memFuncs.addMember(self.username)
        else:    
            print("You are not authorized to add a member")

    def update_password(self):
        if self.is_authorized("consultant"):
            new_password = input("Enter new password: ")
            val = Validation()
            password = val.password_validation(new_password, self.username)
            db = databaseFunctions()
            db.updatePassword(self, password)
        else:
            print("You are not authorized to update password")

    def modify_member(self):
        if self.is_authorized("consultant"):
            memFuncs = MemberFunctions()
            memFuncs.modifyMember(self.username)
        else:
            print("You are not authorized to modify member")

    def find_member(self):
        if self.is_authorized("consultant"):
            search_key = input("Enter search key for finding your member: ")
            memFuncs = MemberFunctions()
            matching_members = memFuncs.search_member(self.username, search_key)

            if matching_members is not None:

                print("Matching member(s) found! ")
                # headers = ["ID", "First Name", "Last Name", "Age", "Gender", "Weight", "Street Address", "Housenumber", "Zip Code", "City", "Phonenumber", "Email", "Registration Date"]
                # table_data = []
                # for member in matching_members:
                #     print("member: ", member)
                #     table_data.append(member)
                # print(tabulate(table_data, headers, tablefmt="pretty"))
            else:
                print("No matching member found")
        else:
            print("You are not authorized to find member")      

    
class Consultant(User):
    def __init__(self, id, first_name, last_name, username, password, registration_date, role = "consultant"):
        super().__init__(id, first_name, last_name, username, password, registration_date, role)
       
