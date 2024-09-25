import sqlite3
import datetime
from validation.inputvalidation import Validation
from random import randint 
from tabulate import tabulate
from database.databaseFunctions import databaseFunctions
from database.logFunction import LogFunction    

class MemberFunctions(databaseFunctions):
    
    def __init__(self):
        super().__init__()

    def queryMembersAll(self):
            from validation.encrypt import decrypt_message
            self.openConnection()
            query = '''
                SELECT  id, 
                        first_name, 
                        last_name, 
                        age, 
                        gender, 
                        weight, 
                        street_address, 
                        house_number, 
                        zip_code, 
                        city, 
                        phone_number, 
                        email
                FROM member;
            '''
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            
            decrypted_data = []
            for row in data:
                decrypted_row = list(row)  # Convert tuple to list for mutable operation
                decrypted_row[1] = decrypt_message(row[1])  # Decrypt first_name
                decrypted_row[2] = decrypt_message(row[2]) 
                decrypted_row[3] = decrypt_message(row[3])
                decrypted_row[4] = decrypt_message(row[4])
                decrypted_row[5] = decrypt_message(row[5])
                decrypted_row[6] = decrypt_message(row[6])
                decrypted_row[7] = decrypt_message(row[7])
                decrypted_row[8] = decrypt_message(row[8])
                decrypted_row[9] = decrypt_message(row[9])
                decrypted_row[10] = decrypt_message(row[10])
                decrypted_row[11] = decrypt_message(row[11])
                decrypted_data.append(decrypted_row)
            headers = ['id', 'first_name', 'last_name', 'age', 'gender', 'weight', 'street_address', 'house_number', 'zip_code', 'city', 'phone_number', 'email']
            print(tabulate(decrypted_data, headers=headers, tablefmt='pretty'))

            #not sure if thise closeconnection is needed
            self.closeConnection()

            return decrypted_data
    
    def addMember(self, username):
            #TODO: input check functies maken en toepassen
            validator = Validation()

            errorCounter = 0
            
            print("You've chosen to add a member")
            firstname = input("Enter firstname:")

            while not validator.name_validation(firstname, username):
                print("Invalid firstname.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                firstname = input("Enter firstname:")
            firstname = firstname.capitalize()
            print(firstname)

            lastname = input("Enter lastname:")
            while not validator.name_validation(lastname, username):
                print("Invalid lastname.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                lastname = input("Enter lastname:")
            lastname = lastname.capitalize()
            print(lastname)

            age = input("Enter age:")
            while not validator.age_validation(age, username):
                print("Invalid age.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                age = input("Enter age:")
            print(age)

            genderInput = input("Enter gender:")
            while not validator.gender_validation(genderInput, username):
                print("Invalid gender.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                genderInput = input("Enter gender:")
            genderInput = genderInput.upper()
            print(genderInput)

            weight = input("Enter weight:")
            while not validator.weight_validation(weight, username):
                print("Invalid weight.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                weight = input("Enter weight:")
            print(weight)

            street = input("Enter street:")
            while not validator.streetname_validation(street, username):
                print("Invalid street.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                street = input("Enter street:")
            street = street.capitalize()
            print(street)

            houseNr = input("Enter house number:")
            while not validator.housenumber_validation(houseNr, username):
                print("Invalid house number.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                houseNr = input("Enter house number:")
            print(houseNr)

            zipCode = input("Enter zip code:")
            while not validator.zipcode_validation(zipCode, username):
                print("Invalid zip code.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                zipCode = input("Enter zip code:")
            print(zipCode)

            print("Choose city:")
            list_city = ['Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Maastricht', 'Den Haag', 'Eindhoven', 'Tilburg', 'Breda', 'Arnhem']
            for index, city in enumerate(list_city):
                print(f"{index + 1}. {city}")
            city = input()
            while not validator.city_validation(city, username):
                print("Invalid city.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                city = input("Choose city:")
            city = list_city[int(city)-1]
            print(city)

            phoneNr = input("Enter phone number Should in the format +31-6-xxxxxxxx:")
            while not validator.phonenumber_validation(phoneNr, username):
                print("Invalid phone number.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                phoneNr = input("Enter phone number:")
            print(phoneNr)

            
            email = input("Enter email:")
            while not validator.email_validation(email, username):
                print("Invalid email.")
                errorCounter += 1
                if errorCounter == 3:
                    print("Too many attempts. Exiting...")
                    return
                email = input("Enter email:")
            print(email)

            self.addMemberQuery(firstname, lastname, age, genderInput, weight, street, houseNr, zipCode, city, phoneNr, email, username)

    def addMemberQuery(self, firstnameInput, lastnameInput, ageInput, genderInput, weightInput, streetInput, houseNrInput, zipCodeInput, cityInput, phoneNrInput, emailInput, username):
        from validation.encrypt import encrypt_message
        self.openConnection()
        Logger = LogFunction()
        randomID = MemberFunctions.memberid_random()
        try:
            current_date = datetime.datetime.now()
            encrypted_firstname = encrypt_message(firstnameInput)
            encrypted_lastname = encrypt_message(lastnameInput)
            encrypted_age = encrypt_message(str(ageInput))
            encrypted_gender = encrypt_message(genderInput)
            encrypted_weight = encrypt_message(str(weightInput))
            encrypted_street = encrypt_message(streetInput)
            encrypted_houseNr = encrypt_message(str(houseNrInput))
            encrypted_zipCode = encrypt_message(zipCodeInput)
            encrypted_city = encrypt_message(cityInput)
            encrypted_phoneNr = encrypt_message(phoneNrInput)
            encrypted_email = encrypt_message(emailInput)
            query = '''
            INSERT INTO member (id, first_name, last_name, age, gender, weight, street_address, house_number, zip_code, city, phone_number, email, registration_date)
            VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            '''
            self.db.execute(query, (randomID, encrypted_firstname, encrypted_lastname, encrypted_age, encrypted_gender, encrypted_weight, encrypted_street, encrypted_houseNr, encrypted_zipCode, encrypted_city, encrypted_phoneNr, encrypted_email, current_date.strftime("%Y-%m-%d %H:%M:%S")))
            self.db.commit()
            
            Logger.addLogToDatabase(username, encrypt_message("New Member is created"), encrypt_message("Account created for member " + firstnameInput + " " + lastnameInput), encrypt_message("No"))
            self.closeConnection()
            print("Member added successfully.")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        
        finally:
            self.closeConnection()


    def modifyMember(self, username):
        from validation.encrypt import encrypt_message

        self.openConnection()

        #laat alle members zien
        print("You've chosen to modify a member. These are all the members currently in the system: ")
        members = self.queryMembersAll()

        errorCounter = 0
        
        if not members:
            print("No members found.")
            self.closeConnection()
            return
        

        while True:
            print("Enter the ID of the member you want to modify (or 'e' to exit):")
            chosenMember = input()
            #check if input is 'e' to exit
            if chosenMember == 'e' or chosenMember == 'E':
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
                # print("Member ID: " + str(member[0]))

                if member[0] == (chosenMember):
                    print("Member found!")
                    specificMember = member
                    print("Name: " + member[1] + " " + member[2])
                    print("Age: " + str(member[3]))
                    break

            if specificMember is None:
                print("No member found with that ID.")
                return

            print("Member with id " + str(chosenMember) + " found.")
            print(specificMember[1])
            print("which field would you like to modify?")
            fields = ["first name", "last name", "age", 'gender', 'weight', 'streetname', 'house number', 'zip code', 'city', 'phone number', 'email']
            for index, field in enumerate(fields):
                print(f"{index + 1}. {field.capitalize()}")

            input_choice = input()
            Val = Validation()
            if input_choice == '1':
                new_value = ("Enter new first name:")
                while not Val.name_validation(new_value, username):
                    print("Invalid first name.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new first name:")
                new_value = encrypt_message(new_value)
                query = f"UPDATE member SET first_name = ? WHERE id = ?"

            elif input_choice == '2':
                new_value = ("Enter new last name:")
                while not Val.name_validation(new_value, username):
                    print("Invalid last name.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new first name:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET last_name = ? WHERE id = ?"
                
            elif input_choice == '3':
                new_value = input("Enter new age:")
                while not Val.age_validation(new_value, username):
                    print("Invalid age.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new age:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET age = ? WHERE id = ?"

            elif input_choice == '4':
                new_value = input("Enter new gender:")
                while not Val.gender_validation(new_value, username):
                    print("Invalid gender.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new gender")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET gender = ? WHERE id = ?"

            elif input_choice == '5':
                new_value = input("Enter new weight:")
                while not Val.weight_validation(new_value, username):
                    print("Invalid weight.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new weight:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET weight = ? WHERE id = ?"    

            elif input_choice == '6':
                new_value = input("Enter new streetname:")
                while not Val.streetname_validation(new_value, username):
                    print("Invalid streetname.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new streetname:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET street_address = ? WHERE id = ?"

            elif input_choice == '7':
                new_value = input("Enter new house number:")
                while not Val.housenumber_validation(new_value, username):
                    print("Invalid house number.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new house number:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET house_number = ? WHERE id = ?"

            elif input_choice == '8':
                new_value = input("Enter new zip code:")
                while not Val.zipcode_validation(new_value, username):
                    print("Invalid zip code.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new zip code:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET zip_code = ? WHERE id = ?"

            elif input_choice == '9':
                print("Choose city:")
                list_city = ['Amsterdam', 'Rotterdam', 'Utrecht', 'Groningen', 'Maastricht', 'Den Haag', 'Eindhoven', 'Tilburg', 'Breda', 'Arnhem']
                for index, city in enumerate(list_city):
                    print(f"{index + 1}. {city}")
                new_value = input("Choose new city:")
                while not Val.city_validation(new_value, username):
                    print("Invalid city.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Choose new city:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET city = ? WHERE id = ?"

            elif input_choice == '10':
                new_value = input("Enter new phone number:")
                while not Val.phonenumber_validation(new_value, username):
                    print("Invalid phone number.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new phone number:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET phone_number = ? WHERE id = ?"

            elif input_choice == '11':
                new_value = input("Enter new email:")
                while not Val.email_validation(new_value, username):
                    print("Invalid email.")
                    errorCounter += 1
                    if errorCounter == 3:
                        print("Too many attempts. Exiting...")
                        return
                    new_value = input("Enter new email:")
                new_value = encrypt_message(new_value) 
                query = f"UPDATE member SET email = ? WHERE id = ?"
            
            self.openConnection()
            self.cursor.execute(query, (new_value, specificMember[0]))
            self.db.commit()
            Logger = LogFunction()
            
            Logger.addLogToDatabase(username, encrypt_message("User is modified"), encrypt_message("User that you modified is: " + (specificMember[1])), encrypt_message("No"))
            print("Member updated successfully.")
            self.closeConnection()  

            
    def search_member(self, username, search_key):

        allMembsQuery = self.queryMembersAll()
        filtered_results = [
            member for member in allMembsQuery
            if search_key in str(member[0]).lower() or  # Assuming member[0] is id, convert to str for comparison
                search_key in member[1].lower() or  # first_name
                search_key in member[2].lower() or  # last_name
                search_key in str(member[3]).lower() or  # age, assuming it's not already a string
                search_key in member[4].lower() or  # gender
                search_key in str(member[5]).lower() or  # weight, assuming it's not already a string
                search_key in member[6].lower() or  # street_address
                search_key in str(member[7]).lower() or  # house_number, convert to str for comparison
                search_key in member[8].lower() or  # zip_code
                search_key in member[9].lower() or  # city
                search_key in member[10].lower() or  # phone_number
                search_key in member[11].lower()  # email
            ]

        return filtered_results

        # print("All members test: ")
        # print(allMembsQuery)
        # self.openConnection()
        # query = '''
        #     SELECT * FROM member
        #     WHERE 
        #     id LIKE ? OR
        #     first_name LIKE ? OR
        #     last_name LIKE ? OR
        #     age LIKE ? OR
        #     gender LIKE ? OR
        #     weight LIKE ? OR
        #     street_address LIKE ? OR
        #     house_number LIKE ? OR
        #     zip_code LIKE ? OR
        #     city LIKE ? OR
        #     phone_number LIKE ? OR
        #     email LIKE ?;
        # '''
        # search_key = f"%{search_key}%"
        # self.cursor.execute(query, (search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key))
        # search_results = self.cursor.fetchall()
        # return search_results

        
    def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)


    def memberid_random():
        year = datetime.date.today().year
        last_digits = year % 100
        randomint = MemberFunctions.random_with_N_digits(7)
        test = str(last_digits) + str(randomint)
        checksum_digit = sum(map(int, str(test))) % 10
        memberid = test + str(checksum_digit)
        print(memberid)
        return memberid

    