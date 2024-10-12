
from database.databaseFunctions import databaseFunctions
from database.consultantFunctions import ConsultantFunctions
from database.memberFunctions import MemberFunctions
from validation.inputvalidation import Validation
from database.logFunction import LogFunction
from tabulate import tabulate
import sqlite3
import datetime
import random
import string
from models.admin import Admin
class AdminFunctions(databaseFunctions):
    
    def __init__(self):
        super().__init__()
    

    def queryConsultantsAll(self):
        from validation.encrypt import decrypt_message


        print("These are all the consultants currently in the system: ")
        self.openConnection()
        query = '''
                SELECT  id, 
                        first_name, 
                        last_name, 
                        username,
                        registration_date  
                FROM consultant
            '''
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # self.closeConnection()

        decrypted_data = []
        for row in data:
            decrypted_row = list(row)
            decrypted_row[1] = decrypt_message(decrypted_row[1])
            decrypted_row[2] = decrypt_message(decrypted_row[2])
            decrypted_row[3] = decrypt_message(decrypted_row[3])
            decrypted_row[4] = decrypted_row[4]
            decrypted_data.append(decrypted_row)
            
        headers = ["ID", "First Name", "Last Name", "Username", "Registration Date"]
        formatdata = tabulate(decrypted_data, headers=headers, tablefmt="pretty")
        print(formatdata)
        return decrypted_data
    

    def generate_temporary_password(self, length=12):
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return temp_password


    def reset_consultant_password(self, user):
        from validation.encrypt import encrypt_message
        logger = LogFunction()
        temporary_password = self.generate_temporary_password()
        self.openConnection()
        # Show all the consultants
        consultants = self.queryConsultantsAll()

        if not consultants:
            print("No Consultants found.")
            self.closeConnection()
            return
        
        while True:
            chosenConsultant = input("Enter the ID of the member you want to get a temporary password for (or 'e' to exit):").lower()
            if chosenConsultant == 'e':
                print("Exiting...")
                self.closeConnection()
                break
            
            try:
                chosenConsultant = int(chosenConsultant)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue  
            if chosenConsultant < 1:
                print("Invalid input. Please enter a number greater than 0.")
                continue  
            
            specificConsultant = None
            for consultant in consultants:
                print("Member ID: " + str(consultant[0]))

                if consultant[0] == (chosenConsultant):
                    print("Member found!")
                    print("Name: " + consultant[1] + " " + consultant[2])

                    specificConsultant = consultant

                    break

            if specificConsultant is None:
                print("ID does not exist in the members list. Please try again.")
                return


            print("Temporary password for this consultant? to quit press 'e' otherwise enter to make a temporary password")
            delete = input().lower()
            if delete == 'e':
                break
            query = f"UPDATE consultant SET password = ? WHERE id = ?"
            self.openConnection()
            self.db.execute(query, (temporary_password, specificConsultant[0]))
            self.db.commit()
            print("Temporary password for consultant: " + specificConsultant[3] + " is: " + temporary_password)
            logger.addLogToDatabase(user.username, encrypt_message("Reset a consultant password"), encrypt_message("Consultant username: " + str(specificConsultant[3])), encrypt_message("No"))
            self.closeConnection()
    


    def add_consultant(self, user, firstname, lastname, username, password):
            from validation.encrypt import encrypt_message

            from validation import authorization


            logger = LogFunction()
            data = datetime.datetime.now()

            self.openConnection()
            encrypted_firstname = encrypt_message(firstname)
            encrypted_lastname = encrypt_message(lastname)
            encrypted_username = encrypt_message(username)
            hashed_password = authorization.hash_password(password)
            try:
                query = '''
                INSERT INTO consultant (first_name, last_name, username, password, registration_date)
                VALUES(?, ?, ?, ?, ?);
                '''
                self.db.execute(query, (encrypted_firstname, encrypted_lastname, encrypted_username, hashed_password, data))
                self.db.commit()
                print("Consultant added successfully.", firstname, lastname, username)
                logger.addLogToDatabase(user.username, encrypt_message("Added a new consultant"), encrypt_message("Username: " + username), encrypt_message("No"))
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            finally:
                self.closeConnection()
            
            
    def modify_consultant(self, user):
        logger = LogFunction()
        from validation.encrypt import encrypt_message
        from validation import authorization

        
        self.openConnection()

        # Show all the consultants
        print("You've chosen to modify a consultant. These are all the consultants currently in the system: ")
        consultants = self.queryConsultantsAll()

        errorCounter = 0
        
        if not consultants:
            print("No members found.")
            self.closeConnection()
            return
        
        while True:
            print("Enter the ID of the member you want to modify (or 'e' to exit):")
            chosenConsultant = input()
            if str(chosenConsultant).lower() == 'e':
                print("Exiting...")
                self.closeConnection()
                break
            
            try:
                chosenConsultant = int(chosenConsultant)
            except ValueError:
                print("Invalid input. Please enter a number.")
                self.closeConnection()
                break
            
            specificConsultant = None
            for consultant in consultants:


                if consultant[0] == (chosenConsultant):
                    print("Consultant found!")
                    print("Name: " + consultant[1] + " " + consultant[2])

                    specificConsultant = consultant


                    break

            if specificConsultant is None:
                print("No consultant found with that ID")
                return
                
            # print("DEBUG: GEBRUIKEN WE DIT?")
            
            print("Consultant with id " + str(chosenConsultant) + " found.")
            print(specificConsultant[1])
            print("which field would you like to modify?")
            fields = ["First name", "Last name", "Username", "Password"]
            for i, field in enumerate(fields):
                print(f"{i+1}. {field}")

            self.openConnection()
            input_choice = input()
            Val = Validation()

            if input_choice == '1':
                new_value = input("Enter new first name:")
                while not Val.name_validation(new_value, user.username):
                    print("Invalid input. Please enter a valid name.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter new first name:")

                new_value = encrypt_message(new_value)
                query = f"UPDATE consultant SET first_name = ? WHERE id = ?"

            elif input_choice == '2':
                new_value = input("Enter new last name:")
                while not Val.name_validation(new_value, user.username):
                    print("Invalid input. Please enter a valid name.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter new last name:")
                new_value = encrypt_message(new_value)
                query = f"UPDATE consultant SET last_name = ? WHERE id = ?"

            elif input_choice == '3':
                new_value = input("Enter new username:")
                while not Val.username_validation(new_value, user.username):
                    print("Invalid input. Please enter a valid username.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter new username:")
                new_value = encrypt_message(new_value)
                query = f"UPDATE consultant SET username = ? WHERE id = ?"

            elif input_choice == '4':
                new_value = input("Enter new password:")
                while not Val.password_validation(new_value, user.username):
                    print("Invalid input. Please enter a valid password.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter new password:")
                new_value = authorization.hash_password(new_value)
                query = f"UPDATE consultant SET password = ? WHERE id = ?"

            

            self.db.execute(query, (new_value, specificConsultant[0]))
            self.db.commit()
            print("Consultant modified successfully.")

            logger.addLogToDatabase(user.username, encrypt_message("Modified a consultant"), encrypt_message("Consultant username: " + str(specificConsultant[3])), encrypt_message("No"))
            self.closeConnection()

            

    def delete_consultant(self, user):
        from validation.encrypt import encrypt_message


        
        logger = LogFunction()
        self.openConnection()
        # Show all the consultants

        print("You've chosen to delete a consultant. These are all the consultants currently in the system: ")
        consultants = self.queryConsultantsAll()

        if not consultants:
            print("No consultants found.")
            self.closeConnection()
            return
        
        while True:
            chosenConsultant = input("Enter the ID of the consultant you want to delete (or 'e' to exit):").lower()
            if chosenConsultant == 'e':
                print("Exiting...")
                self.closeConnection()
                break
            
            try:
                chosenConsultant = int(chosenConsultant)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue    
            
            specificConsultant = None
            for consultant in consultants:
                print("Consultant ID: " + str(consultant[0]))

                if consultant[0] == (chosenConsultant):
                    print("Consultant found!")
                    print("Name: " + consultant[1] + " " + consultant[2])

                    specificConsultant = consultant


                    print("Given ID exists in the consultant list.")
                    break

            if specificConsultant is None:
                print("ID does not exist in the Consultant list. Please try again.")
                return

            print("Consultant with id " + str(chosenConsultant) + " found.")
            print(specificConsultant[1])

            delete = input("Delete this consultant? to quit press 'e' other wise enter to delete").lower()
            if delete == 'e':
                break
            query = f"DELETE FROM consultant WHERE id = ?"
            self.openConnection()
            self.db.execute(query, (specificConsultant[0],))
            self.db.commit()
            print("Consultant deleted successfully.")
            logger.addLogToDatabase(user.username, encrypt_message("Deleted a consultant"), encrypt_message("Consultant username: " + str(specificConsultant[3])), encrypt_message("No"))
            
            self.closeConnection()
    
        
    def delete_member(self, user):
        logger = LogFunction()
        self.openConnection()
        # Show all the consultants
        memfunc = MemberFunctions()
        from validation.encrypt import encrypt_message
        

        print("You've chosen to delete a member. These are all the members currently in the system: ")
        members = memfunc.queryMembersAll()

        if not members:
            print("No members found.")
            self.closeConnection()
            return
        
        while True:
            chosenMember = input("Enter the ID of the member you want to delete (or 'e' to exit):")
            if chosenMember == 'e':
                print("Exiting...")
                self.closeConnection()
                break
            
            try:
                chosenMember = int(chosenMember)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue    
            
            specificMember = None
            for member in members:


                if member[0] == (chosenMember):
                    print("Member found!")
                    print("Name: " + member[1] + " " + member[2])

                    specificMember = member


                    # print("Given ID exists in the member list.")
                    break

            if specificMember is None:
                print("ID does not exist in the members list. Please try again.")
                return

            print("Member with id " + str(chosenMember) + " found.")
            print(specificMember[1])

            delete = input("Delete this member? to quit press 'e' otherwise enter to delete").lower()
            if delete == 'e':
                break
            query = f"DELETE FROM member WHERE id = ?"
            self.openConnection()
            self.db.execute(query, (specificMember[0],))
            self.db.commit()
            print("Member deleted successfully.")
            logger.addLogToDatabase(user.username, encrypt_message("Deleted a member"), encrypt_message("Members name: " + str(specificMember[1] + " " + str(specificMember[2]) )), encrypt_message("No"))
            self.closeConnection()
      
        

    def create_backup(self):
        from database.backupFunctions import BackupFunctions
        backup = BackupFunctions()
        backup.createBackup()

    def restore_backup(self):
        from database.backupFunctions import BackupFunctions
        backup = BackupFunctions()
        backup.restoreBackup()
        


 