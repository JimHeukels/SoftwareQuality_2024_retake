import sys

# should be able to update their own password
# should be able to view a list of users, including their role within the system
# should be able to add new consultants
# should be able to modify consultants
# should be able to delete consultants
# should be able to request a temporary password for consultants
# should be able to create backups of the data in the system and restore old backups
# should be able to view log files
# should be able to add new members
# should be able to modify members
# should be able to delete members from the system (a consultant cannot do this explicitly, they can only modify)
# should be able to search for members within the system

class AdminScreen:
    def __init__(self, user):
        self.user = user

    def displayAdminScreen(self):
        print("Admin Screen")
        fields = ["Update Password", "View Users", "Add Consultant", "Modify Consultant", "Delete Consultant", "Request Temporary Password for Consultant", "Create Backup", "Restore Backup", "View Logs", "Add Member", "Modify Member", "Delete Member", "Retrieve information on a member", "Exit"]
        for index, field in enumerate(fields):
            print(f"{index + 1}. {field}")
        choice = input("Enter your choice: ")
        if choice == '1':
            self.user.update_password()
            self.displayAdminScreen()
        elif choice == '2':
            self.user.show_users()
            self.displayAdminScreen()
        elif choice == '3':
            self.user.add_consultant()
            self.displayAdminScreen()
        elif choice == '4':
            self.user.modify_consultant()
            self.displayAdminScreen()
        elif choice == '5':
            self.user.delete_consultant()
            self.displayAdminScreen()
        elif choice == '6':
            self.user.request_temporary_password()
            self.displayAdminScreen()
        elif choice == '7':
            self.user.create_backup()
            self.displayAdminScreen()
        elif choice == '8':
            self.user.restore_backup()
            self.displayAdminScreen()
        elif choice == '9':
            self.user.view_logs()
            self.displayAdminScreen()
        elif choice == '10':
            self.user.add_member()
            self.displayAdminScreen()
        elif choice == '11':
            self.user.modify_member()
            self.displayAdminScreen()
        elif choice == '12':
            self.user.delete_member()
            self.displayAdminScreen()
        elif choice == '13':
            self.user.find_member()
        elif choice == '14':
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

