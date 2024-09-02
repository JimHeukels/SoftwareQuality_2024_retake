# Should be able to view a list of users including their role within the system
# Should be able to create a backup of the system and restore older backups
# Should be able to view log files
# Should be able to perform the following actions for consultants:
#    - add
#    - modify
#    - delete
#    - request temporary password
# Should be able to perform the following actions for admins:
#    - add
#    - modify
#    - delete
#    - request temporary password
# Should be able to perform the following actions for members:
#    - add
#    - modify
#    - delete
#    - search

class SuperAdminScreen:
    def __init__(self, user):
        self.user = user
        
    def displaySuperAdminScreen(self):

        print("Superadmin Screen")
        fields = ['Update Password', 'View Users', 'Add Consultant', 'Modify Consultant', 'Delete Consultant', 'Request Temporary Password for Consultant', 'Create Backup', 'Restore Backup', 'View Logs', 'Add Member', 'Modify Member', 'Delete Member', 'Retrieve information on a member', 'Add a new admin to the system', 'Modify an existing admin', 'Delete an existing admin', 'Reset an existing admin\'s password', 'Logout', 'Exit']
        for index, field in enumerate(fields):
            print(f"{index + 1}. {field}")

        userInput = input()

        if userInput == "1":
            self.user.update_password()
            self.displaySuperAdminScreen()
        elif userInput == "2":
            self.user.show_users()
            self.displaySuperAdminScreen()
        elif userInput == "3":
            self.user.add_consultant()
            self.displaySuperAdminScreen()
        elif userInput == "4":
            self.user.modify_consultant()
            self.displaySuperAdminScreen()
        elif userInput == "5":
            self.user.delete_consultant()
            self.displaySuperAdminScreen()
        elif userInput == "6":
            self.user.request_temporary_password()
            self.displaySuperAdminScreen()
        elif userInput == "7":
            self.user.create_backup()
            self.displaySuperAdminScreen()
        elif userInput == "8":
            self.user.restore_backup()
            self.displaySuperAdminScreen()
        elif userInput == "9":
            self.user.view_logs()
            self.displaySuperAdminScreen()
        elif userInput == "10":
            self.user.add_member()
            self.displaySuperAdminScreen()
        elif userInput == "11":
            self.user.modify_member()
            self.displaySuperAdminScreen()
        elif userInput == "12":
            self.user.delete_member()
            self.displaySuperAdminScreen()
        elif userInput == "13":
            self.user.find_member()
            self.displaySuperAdminScreen()

        #TODO: implement deze superadmin functies
        elif userInput == "14":
            self.user.add_admin()
            self.displaySuperAdminScreen()
        elif userInput == "15":
            self.user.modify_admin()
            self.displaySuperAdminScreen()
        elif userInput == "16":
            self.user.delete_admin()
            self.displaySuperAdminScreen()
        elif userInput == "17":
            self.user.request_temporary_admin_password()
            self.displaySuperAdminScreen()

        elif userInput == "19":
            exit()
        else:
            print("Invalid input. Please try again.")


