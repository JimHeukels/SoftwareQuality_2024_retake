from database.databaseFunctions import databaseFunctions

#from screens.adminScreen import AdminScreen
from screens.consultantScreen import ConsultantScreen 
from screens.adminScreen import AdminScreen
from screens.superAdminScreen import SuperAdminScreen



class homeScreen():


    @staticmethod
    def homeScreen():
        db_func = databaseFunctions()
        db_func.setup_database()
        from models.consultant import Consultant
        from models.admin import Admin
        from models.superadmin import SuperAdmin


        print("Welcome to the Unique Meal Planner application!")
        print("What would you like to do?")
        print("[1] Login")
        print("[2] Exit program")


        userInput = input()
        print(userInput)

        if(userInput == "1"):
                    

            
            user = db_func.login()
            # print("Homescreen print user")

            
            #if user is a consultant
            if(user != None):
                if type(user) == Consultant:
                    consultant_screen = ConsultantScreen(user)
                    consultant_screen.displayConsultantScreen()
                if type(user) == Admin:
                    admin_screen = AdminScreen(user)
                    admin_screen.displayAdminScreen()
                if type(user) == SuperAdmin:
                    super_admin_screen = SuperAdminScreen(user)
                    super_admin_screen.displaySuperAdminScreen()
            else:
                print("Invalid username or password")
                homeScreen.homeScreen()

        elif(userInput == 2):
            print("Goodbye!")
            exit()

