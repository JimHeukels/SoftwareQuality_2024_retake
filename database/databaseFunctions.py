import sqlite3
from tabulate import tabulate
from database.logFunction import LogFunction



class databaseFunctions:
    
    def __init__(self):
        self.db = None
        self.cursor = None
        
    
    def openConnection(self):
        if self.db is None:
            self.db = sqlite3.connect('uniqueMeal.db')
            self.cursor = self.db.cursor()
   
    
    def closeConnection(self):
        if self.db is not None:
            self.cursor.close()
            self.db.close()
            self.db = None
            self.cursor = None

      

    def login(self):
            from validation.inputvalidation import Validation
            from validation.encrypt import encrypt_message

            from validation.authorization import validate_password
            from models.consultant import Consultant
            from validation.authorization import hash_password

            from models.admin import Admin
            from models.superadmin import SuperAdmin

            logger = LogFunction()


            val = Validation()
            logger = LogFunction()


            self.openConnection()
            counter = 0
  
            usernames_all = self.queryAllUsers()

            while True:
                
                print("Please enter your username:" + "\n")
                username = val.username_login_validation(input())
                password = input("Please enter your password:" + "\n")

                if counter > 3:
                    print("Too many failed login attempts. Log in attempt flagged.")
                    logger.addLogToDatabase(encrypt_message("unknown"), encrypt_message("Unsuccessful login attempt"), encrypt_message("Multiple usernames and password tried"), encrypt_message("Yes"))
                    self.closeConnection()
                    break

                for user_data in usernames_all:
                    if user_data[1] == username:
                        #get the password from the database from the id of the user_data[1]
                        roles = ['admin', 'consultant', 'superadmin']
                        user = None

                        for role in roles:
                            query = f"SELECT * FROM { role } WHERE id = ?"
                            self.openConnection()

                            self.cursor.execute(query, (user_data[0],))
                            result = self.cursor.fetchone()

                            if(result):
                                

                                passwordHashed = hash_password(password)
                                if role == 'admin':
                                    # print("Admin role found")
                                    if validate_password(passwordHashed, result[4]):     
                                        user = Admin(result[0], result[1], result[2], result[3], result[4], result[5])

                                        print("Admin validate password succeeded")     
                                        logger.addLogToDatabase(encrypt_message(username), encrypt_message("logged in"), encrypt_message(""), encrypt_message("No"))
                                        self.closeConnection()
                                        return user
                                elif role == 'consultant':
                                    if validate_password(passwordHashed, result[4]): 
                                        user = Consultant(result[0], result[1], result[2], result[3], result[4], result[5])
                                        print("Consultant validate password succeeded")
                                        logger.addLogToDatabase(encrypt_message(username), encrypt_message("logged in"), encrypt_message(""), encrypt_message("No"))
                                        self.closeConnection()
                                        return user
                                elif role == 'superadmin':
                                    if validate_password(passwordHashed, result[4]):
                                        user = SuperAdmin(result[0], result[1], result[2], result[3], result[4], result[5])
                                        print("Superadmin validate password succeeded")
                                        logger.addLogToDatabase(encrypt_message(username), encrypt_message("logged in"), encrypt_message("succesfull login"), encrypt_message("No"))
                                        self.closeConnection()
                                        return user
                            else:
                                print("Incorrect login information. Please try again.")
                                

                print("Incorrect login information. Please try again.")
                counter += 1


                self.closeConnection()
                        
                
                
                





            
    def updatePassword(self, user, password):
        from models.consultant import Consultant
        from models.admin import Admin
        from models.superadmin import SuperAdmin
        from validation.authorization import hash_password

        from validation.encrypt import encrypt_message

        logger = LogFunction()
        



        self.openConnection()
        # encrypted_username = encrypter.encrypt_message(user.username)
        print(user.username)
        if isinstance(user, Consultant):
            query = f"UPDATE consultant SET password = ? WHERE username = ?"
            new_password = hash_password(password)
            self.db.execute(query, (new_password, user.username))
            self.db.commit()
            logger.addLogToDatabase(user.username, encrypt_message("password updated"), encrypt_message(""), encrypt_message("No"))
            self.closeConnection()
        elif isinstance(user, Admin):
            query = f"UPDATE admin SET password = ? WHERE username = ?"
            new_password = hash_password(password)
            self.db.execute(query, (new_password, user.username))
            self.db.commit()
            logger.addLogToDatabase(user.username, encrypt_message("password updated"), encrypt_message(""), encrypt_message("No"))
            self.closeConnection()
        elif isinstance(user, SuperAdmin):
            query = f"UPDATE superadmin SET password = ? WHERE username = ?"
            new_password = hash_password(password)
            self.db.execute(query, (new_password, user.username))
            self.db.commit()
            logger.addLogToDatabase(user.username, encrypt_message("password updated"), encrypt_message(""), encrypt_message("No"))
            self.closeConnection()
        else:
            logger.addLogToDatabase(encrypt_message("unknown"), encrypt_message("Unauthorized password change attempt"), encrypt_message(""), encrypt_message("Yes"))
            self.closeConnection()


      
    def show_user(self):

        from validation.encrypt import decrypt_message

        self.openConnection()
        # select all the consultants, admins and superadmins show their first name, last name, and username and role
        
        query =  '''
            SELECT first_name, last_name, username, 'admin' AS role
            FROM admin
            UNION
            SELECT first_name, last_name, username, 'consultant' AS role
            FROM consultant

            '''
        # i want to add the role to the table i want if it a consultant, admin or superadmin
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        decrypted_data = []
        for row in data:
            decrypted_data.append([decrypt_message(row[0]), decrypt_message(row[1]), decrypt_message(row[2]), row[3]])
        headers = ['first_name', 'last_name', 'username', 'role']
        print(tabulate(decrypted_data, headers=headers, tablefmt='pretty'))
        self.closeConnection()

    def queryAllUsers(self):
        from validation.encrypt import decrypt_message

        
        # tables = ['admin', 'consultant', 'superadmin']
        tables = ['admin', 'consultant', 'superadmin']

        self.openConnection()

        result = []

        for role in tables:
            query = f"SELECT id, username FROM { role }"
            self.cursor.execute(query, )
            queryResult = self.cursor.fetchall()
            
            if queryResult:
                for user_data in queryResult:
                    result.append(user_data)
        
        self.closeConnection()

        resultDecrypted = []
        for user_data in result:
            decrypted_username = decrypt_message(user_data[1])
            resultDecrypted.append((user_data[0], decrypted_username))

            
        return resultDecrypted
   
    @staticmethod
    def setup_database():
        with sqlite3.connect('uniqueMeal.db') as conn:
            cursor = conn.cursor()

            # create table for users
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS member (
                    id INTEGER PRIMARY KEY NOT NULL,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    age VARCHAR(150) NOT NULL,
                    gender VARCHAR(150) NOT NULL,
                    weight VARCHAR(150) NOT NULL,
                    street_address VARCHAR(150) NOT NULL,
                    house_number VARCHAR(150) NOT NULL,
                    zip_code VARCHAR(150) NOT NULL,
                    city VARCHAR(150) NOT NULL,
                    phone_number VARCHAR(150) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    registration_date VARCHAR(150) NOT NULL
                    )
                """)
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS consultant (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    username VARCHAR(150) NOT NULL,
                    password VARCHAR(150) NOT NULL,
                    registration_date VARCHAR(150) NOT NULL
                    )
                """)
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    username VARCHAR(150) NOT NULL,
                    password VARCHAR(150) NOT NULL,
                    registration_date VARCHAR(150) NOT NULL
                    
                    )
                """)
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS superadmin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    username VARCHAR(150) NOT NULL,
                    password VARCHAR(150) NOT NULL,
                    registration_date VARCHAR(150) NOT NULL
                    
                    )
                """)
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS logging (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date VARCHAR(150) NOT NULL,
                    time VARCHAR(150) NOT NULL,
                    username VARCHAR(150) NOT NULL,
                    activity VARCHAR(150) NOT NULL,
                    additional_info VARCHAR(150) NOT NULL,
                    suspicious VARCHAR(150) NOT NULL
                    
                    )
                """)
            cursor.execute("SELECT COUNT(*) FROM superadmin WHERE id = 1")
            if cursor.fetchone()[0] == 0:
                from validation.encrypt import encrypt_message
                from validation.authorization import hash_password
                from datetime import datetime
                
                # Add a SuperAdmin user if no user with id=1 exists
                hashed_password = hash_password("Admin_123?")
                encrypted_first_name = encrypt_message("Super")
                encrypted_last_name = encrypt_message("Admin")
                encrypted_username = encrypt_message("super_admin")
                try:
                    cursor.execute("""
                        INSERT INTO superadmin (first_name, last_name, username, password, registration_date)
                        VALUES (?, ?, ?, ?, ?)
                    """, (encrypted_first_name, encrypted_last_name, encrypted_username, hashed_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                except sqlite3.IntegrityError:
                    pass  # Ignore if the user already exists
            