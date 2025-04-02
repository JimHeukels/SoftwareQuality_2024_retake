from datetime import datetime
import sqlite3
from tabulate import tabulate
from validation.encrypt import encrypt_message

class LogFunction():
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

    # hieronder de oude logger functie
    # kan nog gebruikt worden indien de nieuwe functie niet goed blijkt te zijn, anders kan deze verwijderd worden
    # def addLogToDatabase(self, username, activity, additional_info, suspicious):
    #     if username == "":
    #         username = encrypt_message("No username was given")
    #     if activity == "":
    #         activity = encrypt_message("No activity was given")
    #     if additional_info == "":
    #         additional_info = encrypt_message("No additional info was given")
    #     if suspicious == "":
    #         suspicious = encrypt_message("No activity indicator was given")

    #     self.openConnection()
    #     try:
    #         current_date = str(datetime.now().date())
    #         time = str(datetime.now().time())
    #         query = '''
    #         INSERT INTO logging (date, time, username, activity, additional_info, suspicious)
    #         VALUES(?, ?, ?, ?, ?, ?);
    #         '''

    #         self.db.execute(query, (current_date, time, username, activity, additional_info, suspicious))

    #         self.db.commit()
    #     except sqlite3.Error as e:
    #         print(f"An error occurred: {e}")
    #     finally:
    #         self.closeConnection()

    # TODO: 
    #   - onderstaande logger functie implementeren in de databaseFunctions class
    #   - op alle plekken waar we de logger aanroepen de parameters aanpassen
    #  
    def addLogToDatabase(self, username=None, activity=None, additional_info=None, suspicious=None):
        # Assign default values only if None is given
        username = encrypt_message(username if username else "No username was given")
        activity = encrypt_message(activity if activity else "No activity was given")
        additional_info = encrypt_message(additional_info if additional_info else "No additional info was given")
        suspicious = encrypt_message(suspicious if suspicious else "No activity indicator was given")

        self.openConnection()
        try:
            current_date = str(datetime.now().date())
            time = str(datetime.now().time())
            query = '''
            INSERT INTO logging (date, time, username, activity, additional_info, suspicious)
            VALUES(?, ?, ?, ?, ?, ?);
            '''

            self.db.execute(query, (current_date, time, username, activity, additional_info, suspicious))
            self.db.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            self.closeConnection()

    def getLogs(self):
        from validation.encrypt import decrypt_message

        self.openConnection()
        try:
            query = '''
            SELECT * FROM logging;
            '''
            self.cursor.execute(query)
            logs = self.cursor.fetchall()
            if logs:
                decrypted_logs = list(map(self.decrypt_log, logs))
                headers = ["Id", "Date", "Time", "Username", "Activity", "Additional Info", "Suspicious"]
                formatdata = tabulate(decrypted_logs, headers, tablefmt="pretty")
                print(formatdata)
            else:
                print("No logs found")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            self.closeConnection()
    
    def decrypt_log(self, log):
        from validation.encrypt import decrypt_message
        # Decrypt only the required parts of the log
        decrypted_part = tuple(decrypt_message(log[i]) for i in range(3, 7))
        # Return the combined result
        return log[:3] + decrypted_part