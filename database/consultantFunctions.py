## file containing all the functions related to the consultant table in the database
from database.memberFunctions import MemberFunctions
from tabulate import tabulate
from database.logFunction import LogFunction
import sqlite3
import datetime


class ConsultantFunctions(MemberFunctions):

    def __init__(self):
        super().__init__()
        # self.db = None
        # self.cursor = None

    def queryConsultantsAll(self):
            print("These are all the consultants currently in the system: ")
            self.openConnection()
            query = "SELECT id, first_name, last_name, username, registration_date  FROM consultant"
            self.cursor.execute(query)
            consultants = self.cursor.fetchall()
            self.closeConnection()
            headers = ["ID", "First Name", "Last Name", "Username", "Registration Date"]
            formatdata = tabulate(consultants, headers=headers, tablefmt="pretty")
            print(formatdata)


    def add_consultant(self, user, firstname, lastname, username, password):
            from models.superadmin import SuperAdmin
            from models.admin import Admin
            logger = LogFunction()
            if isinstance(user, SuperAdmin) or isinstance(user, Admin):
                data = datetime.datetime.now()
                self.openConnection()
                try:
                    query = '''
                    INSERT INTO consultant (first_name, last_name, username, password, registration_date)
                    VALUES(?, ?, ?, ?, ?);
                    '''
                    self.db.execute(query, (firstname, lastname, username, password, data))
                    self.db.commit()
                    print("Consultant added successfully.", firstname, lastname, username)
                    logger.addLogToDatabase(user.username, "Added a new consultant", "Username: " + username, "No")
                except sqlite3.Error as e:
                    print(f"An error occurred: {e}")
                finally:
                    self.closeConnection()
            else:
                logger.addLogToDatabase(user.username, "Unauthorized access", "Tried to add a consultant", "Yes")
                print("You are not authorized to add a consultant.")
                self.closeConnection()


    def modify_consultant(self, user):
            from models.superadmin import SuperAdmin
            from models.admin import Admin

            from validation.inputvalidation import Validation
            from validation.encrypt import encrypt_message


            logger = LogFunction()

            validator = Validation()

            if isinstance(user, SuperAdmin) or isinstance(user, Admin):
                self.openConnection()
                # Show all the consultants
                


                print("You've chosen to modify a consultant. These are all the consultants currently in the system: ")
                print("DEBUG: GEBRUIKEN WE DIT? - modifyconsultant, aangeroepen als consultant")
                consultants = self.queryConsultantsAll()
                
                while True:
                    print("Enter the ID of the member you want to modify (or 'e' to exit):")
                    chosenConsultant = int(input())
                    if str(chosenConsultant).lower() == 'e':
                        break
                    
                    specificConsultant = None
                    for consultant in consultants:


                        if consultant[0] == (specificConsultant):
                            print("Member found!")
                            print("Name: " + consultant[1] + " " + consultant[2])
                            print("Age: " + str(consultant[3]))
                            specificConsultant = consultant

                            print("Given ID exists in the members list.")
                            break

                        else:
                            print("ID does not exist in the members list. Please try again.")
                            
                    print("Consultant with id " + str(chosenConsultant) + " found.")
                    # print("DEBUG: GEBRUIKEN WE DIT?")

                    print(specificConsultant[1])
                    print("which field would you like to modify?")
                    fields = ["First name", "Last name", "username", "password"]
                    for index, field in enumerate(fields):
                        print(f"{index + 1}. {field}")

                    self.openConnection()
                    input_choice = input()
                    if input_choice == '1':
                        new_firstname = validator.name_validation(input("Enter new first name:"))
                        encrypted_firstname = encrypt_message(new_firstname)
                        query = f"UPDATE consultant SET first_name = ? WHERE id = ?"
                        self.db.execute(query, (encrypted_firstname, specificConsultant[0]))
                        self.db.commit()
                    elif input_choice == '2':
                        new_lastname = validator.name_validation(input("Enter new last name:"))
                        encrypted_lastname = encrypt_message(new_lastname)
                        query = f"UPDATE consultant SET last_name = ? WHERE id = ?"
                        self.db.execute(query, (encrypted_lastname, specificConsultant[0]))
                        print(query)
                        self.db.commit()
                    elif input_choice == '3':
                        new_username = validator.username_validation(input("Enter new username:"))
                        encrypted_userame = encrypt_message(new_username)
                        query = f"UPDATE consultant SET username = ? WHERE id = ?"
                        self.db.execute(query, (encrypted_userame, specificConsultant[0]))
                        self.db.commit()
                    elif input_choice == '4':
                        new_password = validator.password_update_validation(input("Enter new password:"))
                        encrypted_password = encrypt_message(new_password)
                        query = f"UPDATE consultant SET password = ? WHERE id = ?"
                        self.db.execute(query, (new_password, specificConsultant[0]))
                        self.db.commit()
                    


                    # logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Modified a consultant"), encrypt_message("Consultant username: " + (specificConsultant[3])), encrypt_message("No"))
                    self.closeConnection()

            else:
                logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Unauthorized access"), encrypt_message("Tried to modify a consultant"), encrypt_message("Yes"))
                print("You are not authorized to modify a consultant.")
                self.closeConnection()

    
    def delete_consultant(self, user):
        from models.superadmin import SuperAdmin
        from models.admin import Admin
        logger = LogFunction()
        if isinstance(user, SuperAdmin) or isinstance(user, Admin):
            self.openConnection()
            # Show all the consultants

            print("You've chosen to delete a consultant. These are all the consultants currently in the system: ")
            consultants = self.queryConsultantsAll()
            
            while True:
                print("Enter the ID of the member you want to delete (or 'e' to exit):")
                chosenConsultant = input()
                if chosenConsultant.lower() == 'e':
                    break
                chosenConsultant = int(chosenConsultant)
                specificConsultant = None
                for consultant in consultants:
                    print(f"Consultant ID: {consultant[0]}")

                    if consultant[0] == (specificConsultant):
                        print("Member found!")
                        print(f"Name: {consultant[1]} {consultant[2]}")
                        print(f"Age: {consultant[3]}")
                        specificConsultant = consultant

                        print("Given ID exists in the members list.")
                        break

                    else:
                        print("ID does not exist in the members list. Please try again.")
                        
                print(f"Consultant with id {chosenConsultant} found.")
                print(specificConsultant[1])
                print("Delete this consultant? to quit press 'e' other wise enter to delete")
                delete = input()
                if delete == 'e':
                    break
                query = f"DELETE FROM consultant WHERE id = ?"
                self.db.execute(query, (specificConsultant[0],))
                self.db.commit()
                print("Consultant deleted successfully.")
                logger.addLogToDatabase(user.username, "Deleted a consultant", "Consultant username: " + str(specificConsultant[3]), "No")
                self.closeConnection()
        else:
            logger.addLogToDatabase(user.username, "Unauthorized access", "Tried to delete a consultant", "Yes")
            print("You are not authorized to delete a consultant.")
            self.closeConnection()
