import sys
from validation.encrypt import decrypt_message
# should be able to update their own password
# should be able to add a new member
# should be able to modify information of existing members
# should be able to search for members

class ConsultantScreen:
    def __init__(self, user):
        self.user = user
        # How to see if the user is a consultant

     
    def displayConsultantScreen(self):
        print("Consultant Screen")
        

        username = decrypt_message(self.user.username)
        print("Welcome " + str(username) + "\n")
        fields = ["Update Password", "Add Member", "Modify Member", "Search Member", "Logout"]
        for index, field in enumerate(fields):
            print(f"{index + 1}. {field}")
        choice = input("Enter your choice: ")
        if choice == '1':
            self.user.update_password()
            self.displayConsultantScreen()
        elif choice == '2':
            self.user.add_member()
            self.displayConsultantScreen()
        elif choice == '3':
            self.user.modify_member()
            self.displayConsultantScreen()
        elif choice == '4':
            self.user.find_member()
            self.displayConsultantScreen()
        elif choice == '5':
            sys.exit()
        else:
            print("Invalid choice")

