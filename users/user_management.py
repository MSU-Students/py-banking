import random
from account import handle_account_option
from utils import clear_console
import json
import os

class User:
    def __init__(self, User_Id='', pin='', address='', bday='', fullname='', mob_num='', authentication=0,
                 email='', nationality='', approval=0, is_admin=False):
        self.User_Id = User_Id
        self.pin = pin
        self.name = fullname
        self.mobile_number = mob_num
        self.address = address
        self.bday = bday
        self.authentication = authentication
        self.email = email
        self.nationality = nationality
        self.approval = approval
        self.is_admin = is_admin

class UserService:
    registered_user = User()
    login_user = User()
    users_file = "users.json"

    def __init__(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                self.users_data = json.load(file)
        else:
            self.users_data = []
            admin_account = {
                "full_name": "Admin",
                "mobile_num": "0000000000",
                "address": "Head Office",
                "bday": "1970-01-01",
                "email": "admin@example.com",
                "nationality": "None",
                "user_id": "admin",
                "pin": "admin123",
                "approval": 1,
                "authentication": "00000",
                "is_admin": True
            }
            self.users_data.append(admin_account)
            with open(self.users_file, 'w') as f:
                json.dump(self.users_data, f, indent=4)

    def login(self):
        self.user_id = input("User ID:\t\t")
        self.pin = input("Password:\t\t")

        for user in self.users_data:
            if user['user_id'] == self.user_id and user['pin'] == self.pin:
                self.login_user = User(
                    User_Id=user['user_id'],
                    pin=user['pin'],
                    address=user['address'],
                    bday=user['bday'],
                    fullname=user['full_name'],
                    mob_num=user['mobile_num'],
                    authentication=user['authentication'],
                    email=user['email'],
                    nationality=user['nationality'],
                    approval=user['approval'],
                    is_admin=user.get('is_admin', False)
                )
                return True

        print("Invalid username or pin")
        input("Wrong credentials. Press any key to continue")
        return False

    def register(self):
        print("Register New User (Admin accounts can only be added manually)")
        self.full_name = input("Full Name:\t\t")
        self.mobile_num = input("Mobile Number:\t\t")
        self.address = input("Address:\t\t")
        self.bday = input("Birthdate:\t\t")
        self.email = input("Email Address:\t\t")
        self.nationality = input("Nationality:\t\t")
        self.user_id = input("User ID:\t\t")
        self.pin = input("Password:\t\t")
        self.approval = 0
        self.authentication = str(random.randint(10000, 99999))

        user_data = {
            "full_name": self.full_name,
            "mobile_num": self.mobile_num,
            "address": self.address,
            "bday": self.bday,
            "email": self.email,
            "nationality": self.nationality,
            "user_id": self.user_id,
            "pin": self.pin,
            "approval": self.approval,
            "authentication": self.authentication,
            "is_admin": False
        }

        self.users_data.append(user_data)

        with open(self.users_file, 'w') as account:
            json.dump(self.users_data, account, indent=4)

        self.registered_user = User(self.user_id, self.pin, self.address, self.bday, self.full_name,
                                    self.mobile_num, self.authentication, self.email, self.nationality,
                                    self.approval, False)
        print('You have successfully registered an account!')

    def forgot_password(self):
        print("Enter the correct information for user authentication")
        self.proof_accnum = input('Enter User ID:\t\t')
        self.proof = input('Enter Authentication Code:\t\t')

        for user_data in self.users_data:
            if user_data["user_id"] == self.proof_accnum and user_data["authentication"] == self.proof:
                print("You can now change your password")
                self.pin = input("New Password:\t")
                self.confirm_pin = input("Confirm Password:\t")
                if self.pin == self.confirm_pin:
                    user_data['pin'] = self.pin
                    with open(self.users_file, 'w') as account:
                        json.dump(self.users_data, account, indent=4)
                    print("You have successfully changed your password!")
                    return True
                else:
                    print("Passwords do not match.")
                return
        print("Account or authentication code not found.")
        input("Press any key to continue")

    def view_all_users(self):
        print("\nRegistered Users:")
        if not self.users_data:
            print("No users found.")
        else:
            for index, user in enumerate(self.users_data, 1):
                print(f"\nUser {index}:")
                print(f"  Full Name     : {user['full_name']}")
                print(f"  User ID       : {user['user_id']}")
                print(f"  Email         : {user['email']}")
                print(f"  Mobile Number : {user['mobile_num']}")
                print(f"  Is Admin      : {user.get('is_admin', False)}")
                print(f"  Approved      : {'Yes' if user['approval'] == 1 else 'No'}")

    def approve_users(self):
        print("\n--- Pending Approvals ---")
        pending = [u for u in self.users_data if not u.get("is_admin", False) and u['approval'] == 0]
        if not pending:
            print("No users pending approval.")
            return

        for i, user in enumerate(pending, 1):
            print(f"{i}. {user['full_name']} ({user['user_id']})")
        try:
            choice = int(input("Enter number of user to approve (0 to cancel): "))
            if choice > 0 and choice <= len(pending):
                user = pending[choice - 1]
                user['approval'] = 1
                with open(self.users_file, 'w') as f:
                    json.dump(self.users_data, f, indent=4)
                print(f"User {user['user_id']} approved successfully.")
            elif choice == 0:
                return
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

User_service = UserService()

EXIT, LOGIN, REGISTER, FORGOT_PASS = (0, 1, 2, 3)

def print_main_menu():
    print("Options:")
    print(f"\t{LOGIN} : Login")
    print(f"\t{REGISTER} : Register")
    print(f"\t{FORGOT_PASS} : Forgot Password")
    print(f"\t{EXIT} : Exit")

def handle_admin_menu():
    while True:
        print("\n--- Admin Panel ---")
        print("1. View All Users")
        print("2. Approve Pending Users")
        print("0. Back to Main Menu")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            clear_console()
            User_service.view_all_users()
            input("\nPress Enter to continue...")
            clear_console()
        elif choice == 2:
            clear_console()
            User_service.approve_users()
            input("\nPress Enter to continue...")
            clear_console()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

def handle_user_option():
    option = LOGIN
    while option != EXIT:
        print_main_menu()
        try:
            option = int(input("\n\tCommand: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if option == REGISTER:
            clear_console()
            print("Registration")
            User_service.register()

        elif option == LOGIN:
            clear_console()
            print("Login")
            if User_service.login():
                if User_service.login_user.is_admin:
                    clear_console()
                    print(f"Welcome Admin {User_service.login_user.name}")
                    handle_admin_menu()
                elif User_service.login_user.approval == 0:
                    print("Account hasn't been confirmed by the Admin")
                    input("Press enter to continue")
                else:
                    clear_console()
                    print(f"Welcome {User_service.login_user.name}")
                    handle_account_option()

        elif option == FORGOT_PASS:
            clear_console()
            if User_service.forgot_password():
                User_service.login()

        elif option == EXIT:
            clear_console()
            return

        else:
            print("Invalid option. Please select from the menu.")

        clear_console()