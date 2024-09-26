import sqlite3
import datetime
from tabulate import tabulate
from validation.inputvalidation import Validation
from database.logFunction import LogFunction
from database.databaseFunctions import databaseFunctions



class SuperAdminFunctions(databaseFunctions):

    def __init__(self):
        super().__init__()

    def queryAdminsAll(self):
                from validation.encrypt import decrypt_message

                print("These are all the admins currently in the system: ")

                self.openConnection()
                query = "SELECT id, first_name, last_name, username, registration_date  FROM admin"
                self.cursor.execute(query)
                admins = self.cursor.fetchall()

                decrypted_admins = []

                for row in admins:
                    decrypted_row = list(row)  # Convert tuple to list for mutable operation
                    decrypted_row[1] = decrypt_message(row[1])  # Decrypt first_name
                    decrypted_row[2] = decrypt_message(row[2]) 
                    decrypted_row[3] = decrypt_message(row[3])


                    decrypted_admins.append(decrypted_row)
                headers = ['id', 'first_name', 'last_name', 'username', 'registration_date']
                print(tabulate(decrypted_admins, headers=headers, tablefmt='pretty'))

                self.closeConnection()

                # formatdata = tabulate(admins, headers=headers, tablefmt="pretty")
                # print(formatdata)
                return decrypted_admins
    

    def add_Admin(self, user, firstname, lastname, username, password):
            from validation import encrypt
            from validation import authorization
            from validation.encrypt import encrypt_message

            date = datetime.datetime.now()
            self.openConnection()
            encrypt_firstname = encrypt_message(firstname)
            encrypt_lastname = encrypt_message(lastname)
            encrypt_username = encrypt_message(username)
            hashed_password = authorization.hash_password(password)

            try:
                query = '''
                INSERT INTO admin (first_name, last_name, username, password, registration_date)
                VALUES(?, ?, ?, ?, ?);
                '''
                self.db.execute(query, (encrypt_firstname, encrypt_lastname, encrypt_username, hashed_password ,date))
                self.db.commit()
                print("Admin added successfully.", firstname, lastname, username)
                logger = LogFunction()
                logger.addLogToDatabase(user.username, encrypt_message("Added a new admin"), encrypt_message("Admin username that has been added: " + username), encrypt_message("No"))
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
            finally:
                self.closeConnection()
        

    def modify_admin(self, user):
        from validation.inputvalidation import encrypt_message
        logger = LogFunction()
        validator = Validation()

        self.openConnection()

        print("You've chosen to modify an admin. These are all the admins currently in the system: ")
        admins = self.queryAdminsAll()


        while True:
            print("Enter the ID of the admin you want to modify (or 'e' to exit): ")
            chosenAdmin = input()
            if chosenAdmin.lower() == 'e':
                break
            
            chosenAdmin = int(chosenAdmin)
            specificAdmin = None
            for admin in admins:
                # print("Admin ID: " + str(admin[0]))
                if admin[0] == chosenAdmin:
                    print("Admin found!")
                    specificAdmin = admin
                    break
            if specificAdmin == None:
                print("Admin not found. Please try again.")
                continue

            print("Admin with id " + str(specificAdmin[0]) + " found")
            print(specificAdmin[1])
            print("which field would you like to modify?")
            fields = ["First name", "Last name", "Username", "Password"]
            for index, field in enumerate(fields):
                print(f"{index + 1}. {field}")

            self.openConnection()
            input_choice = input()

            errorCounter = 0

            if input_choice == "1":
                
                new_value = input("Enter the new first name: ")
                while not validator.name_validation(new_value, user.username):
                    print("Invalid name. Please try again.")
                    errorCounter += 1
                    if errorCounter > 2:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter the new first name: ")
                new_value = encrypt_message(new_value)
                query = f"UPDATE admin SET first_name = ? WHERE id = ?"

                # logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Admin modification"), encrypt_message("Admin that you modified is: " + (specificAdmin[1])), encrypt_message("No"))
            elif input_choice == "2":
                new_value = input("Enter the new last name: ")
                while not validator.name_validation(new_value, user.username):
                    errorCounter += 1
                    if errorCounter > 2:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter the new last name: ")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE admin SET last_name = ? WHERE id = ?"

                # logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Admin modification"), encrypt_message("Admin name '" + str(specificAdmin[1])+ " "  + specificAdmin[2] + "', changed to '" + specificAdmin[1] + " " + new_value + "'"), encrypt_message("No"))
            elif input_choice == "3":
                new_value = input("Enter the new username: ")
                while not validator.username_validation(new_value, user.username):
                    errorCounter += 1
                    if errorCounter > 2:
                        print("Too many errors. Exiting...")
                        return
                    new_value = input("Enter the new username: ")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE admin SET username = ? WHERE id = ?"

                # logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Admin modification"), encrypt_message("Admin username changed from " + str(specificAdmin[3])+ " to "  + new_value), encrypt_message("No"))
            elif input_choice == "4":
                new_value = input("Enter the new password: ")
                while not validator.password_validation(new_value, user.username):
                    errorCounter += 1
                    if errorCounter > 2:
                        print("Too many errors. Exiting...")
                        return
                new_value = encrypt_message(new_value)
                query = f"UPDATE admin SET password = ? WHERE id = ?"

                # logger.addLogToDatabase(encrypt_message(user.username), encrypt_message("Admin modification"), encrypt_message("password changed for admin " + specificAdmin[3]), encrypt_message("No"))
            logger.addLogToDatabase(user.username, encrypt_message("User is modified"), encrypt_message("User that you modified is: " + (specificAdmin[1])), encrypt_message("No"))
            self.openConnection()
            self.cursor.execute(query, (new_value, specificAdmin[0]))
            self.db.commit()
            print("Admin updated successfully")
            self.closeConnection()


    def delete_admin(self, user):
        from validation.inputvalidation import encrypt_message
        
        logger = LogFunction()
        self.openConnection()
        # Show all the consultants

        print("You've chosen to delete an admin. These are all the admins currently in the system: ")
        admins = self.queryAdminsAll()
        
        if not admins:
            print("No admins found.")
            return

        while True:
            print("Enter the ID of the admin you want to delete (or 'e' to exit):")
            chosenAdmin = input()
            if chosenAdmin.lower() == 'e':
                break

            chosenAdmin = int(chosenAdmin)
            
            specificAdmin = None
            for admin in admins:
                # print("Member ID: " + str(admin[0]))

                if admin[0] == (chosenAdmin):
                    print("Member found!")
                    print("Name: " + admin[1] + " " + admin[2])
                    print("Age: " + str(admin[3]))
                    specificAdmin = admin


                    break

            if specificAdmin == None:
                print("Admin not found. Please try again.")
                return
                    
            print("Admin with id " + str(chosenAdmin) + " found.")
            print(specificAdmin[1])
            print("Delete this admin? to quit press 'e' otherwise enter to delete")
            delete = input()
            if delete == 'e':
                break
            query = f"DELETE FROM admin WHERE id = ?"
            self.openConnection()
            self.db.execute(query, (specificAdmin[0],))
            self.db.commit()
            print("Admin deleted successfully.")
            logger.addLogToDatabase(user.username, encrypt_message("Deleted a admin"), encrypt_message("Admin username: " + str(specificAdmin[3])), encrypt_message("No"))
            self.closeConnection()


    def request_temporary_admin_password(self, user):
        from database.adminFunctions import AdminFunctions
        from validation.encrypt import encrypt_message
        logger = LogFunction()
        adminFunc = AdminFunctions()
        temporary_password = adminFunc.generate_temporary_password()
        self.openConnection()
        # Show all the consultants
        admins = self.queryAdminsAll()
        if not admins:
            print("No admins found.")
            self.closeConnection()
            return
        
        while True:
            print("Enter the ID of the admin you want to get a temporary password for (or 'e' to exit):")
            chosenAdmin = input()
            if chosenAdmin == 'e' or chosenAdmin == 'E':
                print("Exiting...")
                self.closeConnection()
                break
            
            try:
                chosenAdmin = int(chosenAdmin)
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue    
            

            specificAdmin = None
            for admin in admins:
                # print("Member ID: " + str(admin[0]))

                if admin[0] == (chosenAdmin):
                    print("Member found!")
                    print("Name: " + admin[1] + " " + admin[2])
                    print("Age: " + str(admin[3]))
                    specificAdmin = admin
                    print ("LOOP PRINT: SPECIFIC ADMIN ID: " + str(specificAdmin[0]))

                    print("Given ID exists in the consultant list.")
                    break

            if specificAdmin is None:
                print("ID does not exist in the members list. Please try again.")
                return

            print("Admin with id " + str(specificAdmin) + " found.")
            print(specificAdmin[1])

            print("Generate temporary password for this admin? to quit press 'e' otherwise press Enter to make a temporary password")
            delete = input()
            if delete == 'e':
                break
            query = f"UPDATE admin SET password = ? WHERE id = ?"
            self.openConnection()
            self.db.execute(query, (temporary_password, specificAdmin[0]))
            self.db.commit()
            print("Temporary password for admin: " + specificAdmin[3] + " is: " + temporary_password)
            logger.addLogToDatabase(user.username, encrypt_message("Reset a admin password"), encrypt_message("Consultant username: " + str(specificAdmin[3])), encrypt_message("No"))
            self.closeConnection()