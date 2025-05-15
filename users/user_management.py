import random
from account import handle_account_option
from utils import clear_console
import json
import os
from utils import clear_console

class User:
    def __init__(self, User_Id='', pin='', address='', bday='', fullname='', mob_num='', authentication=0, email='', nationality='', approval=0):
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

    def login(self):
        self.user_id = input("User ID:\t\t")
        self.pin = input("Password:\t\t")
        
        for user_data in self.users_data:
            if user_data['user_id'] == self.user_id and user_data['pin'] == self.pin:
                self.login_user = User(
                    User_Id=user_data["user_id"],
                    pin=user_data["pin"],
                    address=user_data["address"],
                    bday=user_data["bday"],
                    fullname=user_data["full_name"],
                    mob_num=user_data["mobile_num"],
                    authentication=user_data["authentication"],
                    email=user_data["email"],
                    nationality=user_data["nationality"],
                    approval=user_data["approval"]
                )
                return  # Exit after setting up login_user

        print("Invalid username or pin")
        input("Wrong credentials. Press any key to continue")
        clear_console()

    
    def register(self):
        self.full_name = input("Full Name:\t\t")
        self.mobile_num = input("Mobile Number:\t\t")
        self.address = input("Address:\t\t")
        self.bday = input("Birthdate:\t\t")
        self.email = input("Email Address:\t\t")
        self.nationality = input("Nationality:\t\t")
        self.user_id = input("User ID:\t\t")
        self.approval = 0
        self.authentication = str(random.randint(10000, 99999))
        self.pin = input("Password(4 digits):\t")
        if not self.pin.isdigit() or len(self.pin) != 4:
            print("try again...")
            input("press enter to continue...")
            return
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
            "authentication": self.authentication
        }
        self.users_data.append(user_data)

        with open(self.users_file, 'w+') as account:
            json.dump(self.users_data, account, indent=4)

        self.registered_user = User(self.user_id, self.pin, self.address, self.bday, self.full_name, self.mobile_num, self.authentication, self.email, self.nationality, self.approval)
        print('You have successfully registered an account!')
    def forgot_password(self):
        print("Enter the correct information for user authentication")
        self.proof_accnum = input('Enter User User ID:\t\t\t')
        self.proof = input('Enter User Authentication:\t\t')

        user_found = False
        for user_data in self.users_data:
            if user_data["user_id: "] == self.proof_accnum and user_data["authentication: "] == self.proof:
                user_found = True
                self.user_data = user_data
                break

        if user_found:
            print("You can now change your password")
            self.pin = input("New Password(4 digits):\t\t")
            if not self.pin.isdigit() or len(self.pin) != 4:
                print("try again...")
                return
            
            self.confirm_pin = input("Confirm Password:\t\t")

            if self.pin == self.confirm_pin:
                self.user_data['pin: '] = self.pin
                with open(self.users_file, 'w') as account:
                    json.dump(self.users_data, account, indent=4)
                print("You have successfully changed your password!")
                return True
            else:
                print("Passwords do not match.")
        else:
            print("Account or authentication code not found.")
            input("Press any key to continue")

    def change_info(self):
        print("Change Information")
        print("1. Change Address")
        print("2. Change Mobile Number")
        print("3. Change Email Address")
        print("4. Change Nationality")
        print("5. Change Birthdate")

        option = int(input("Select an option: "))
        clear_console()
        print("Change Information")
        if option == 1:
            new_address = input("Enter new address: ")
            self.login_user.address = new_address
        elif option == 2:
            new_mobile_number = input("Enter new mobile number: ")
            self.login_user.mobile_number = new_mobile_number
        elif option == 3:
            new_email = input("Enter new email address: ")
            self.login_user.email = new_email
        elif option == 4:
            new_nationality = input("Enter new Nationality: ")
            self.login_user.nationality = new_nationality
        elif option == 5:
            new_bday = input("Enter new Birthdate: ")
            self.login_user.bday = new_bday
        else:
            for index, user in enumerate(self.users_data, 1):
                print(f"\nUser {index}:")
                print(f"  Full Name : {user['full_name']}")
                print(f"  User ID   : {user['user_id']}")
                print(f"  Email     : {user['email']}")
                print(f"  Phone     : {user['mobile_num']}")
                print(f"  Balance   : ₱{user.get('balance', 0.0):,.2f}")
                print(f"  Admin     : {user.get('is_admin', False)}")
                print(f"  Approved  : {user.get('approved', False)}")
                
    def change_pass(self):
        print("\tCHANGE PIN")
        self.old_pin = input("Enter your previous pin:\t\t")
        if self.old_pin != User_service.login_user.pin:
            print("incorrect pin")
            return
        
        print("you can now change your pin")
        self.new_pin = input("Enter your new pin(4 digits only):\t\t")
        if not self.new_pin.isdigit() or len(self.new_pin) != 4:
            print("please try again")
            input("press enter to continue...")
            return
        self.confirm_pin = input("Re-enter your new pin:\t\t")
        if self.new_pin != self.confirm_pin:
            print("confirmation is incorrect...")
            return
        
        self.login_user.pin = self.new_pin
        for user_data in self.users_data:
            if user_data["user_id"] == self.login_user.User_Id:
                user_data["pin"] = self.login_user.pin
                break

        with open(self.users_file, 'w') as account:
            json.dump(self.users_data, account, indent=4)
        print("Profile information updated successfully!")
        input("Press any key to continue")

    def approve_users(self):
        print("\n--- Approve Users ---")
        pending_users = [u for u in self.users_data if not u.get('approved', False) and not u.get('is_admin', False)]

        if not pending_users:
            print("No users pending approval.")
            return

        for user_data in self.users_data:
            if user_data["user_id"] == self.login_user.User_Id:
                user_data["address"] = self.login_user.address
                user_data["mobile_num"] = self.login_user.mobile_number
                user_data["email"] = self.login_user.email
                user_data["nationality"] = self.login_user.nationality
                user_data["bday"] = self.login_user.bday
                break
        
        with open(self.users_file, 'w') as account:
            json.dump(self.users_data, account, indent=4)
        print("Profile information updated successfully!")
        input("Press any key to continue")

    def change_pass(self):
        print("\tCHANGE PIN")
        self.old_pin = input("Enter your previous pin:\t\t")
        if self.old_pin != User_service.login_user.pin:
            print("incorrect pin")
            return
        
        print("you can now change your pin")
        self.new_pin = input("Enter your new pin(4 digits only):\t\t")
        if not self.new_pin.isdigit() or len(self.new_pin) != 4:
            print("please try again")
            input("press enter to continue...")
            return
        self.confirm_pin = input("Re-enter your new pin:\t\t")
        if self.new_pin != self.confirm_pin:
            print("confirmation is incorrect...")
            return
        
        self.login_user.pin = self.new_pin
        for user_data in self.users_data:
            if user_data["user_id"] == self.login_user.User_Id:
                user_data["pin"] = self.login_user.pin
                break

        with open(self.users_file, 'w') as account:
            json.dump(self.users_data, account, indent=4)
        print("Profile information updated successfully!")
        input("Press any key to continue")


    def view_loans(self):
        
        if self.login_user.is_admin:
            print("\n--- View All Loans ---")
            if not self.loans_data:
                print("No loan records found.")
            else:
                for index, loan in enumerate(self.loans_data, 1):
                    print(f"\nLoan {index}:")
                    print(f"  Loan ID         : {loan.get('loan_id')}")
                    print(f"  User ID         : {loan.get('user_id')}")
                    print(f"  Amount          : ₱{loan.get('amount', 0.0):,.2f}")
                    print(f"  Status          : {loan.get('status', 'Pending')}")
                    print(f"  Repayment Date  : {loan.get('repayment_date', 'N/A')}")
        else:
            print("You must be an admin to view loan records.")

    

User_service = UserService()

EXIT, LOGIN, REGISTER, FORGOT_PASS = (0, 1, 2, 3)

def print_main_menu():
    print("Options:")
    print(f"\t{LOGIN} : Login")
    print(f"\t{REGISTER} : Register")
    print(f"\t{FORGOT_PASS} : Forgot Password")
    print(f"\t{EXIT} : Exit")

def handle_user_option():
    key = False
    global enter
    option = LOGIN
    while option != EXIT:
        print_main_menu()
        option = int(input("\n\tCommand: "))

        if option == REGISTER:
            print("Registration")
            User_service.register()

        elif option == LOGIN:
            print("Login")
            User_service.login()

            user_found = False
            for user_data in User_service.users_data:
                if user_data['user_id'] == User_service.login_user.User_Id and user_data['pin'] == User_service.login_user.pin:
                    user_found = True
                    approval_status = user_data['approval']
                    break

            if not user_found:
                print("Invalid username or pin")
                input("Wrong credentials. Press any key to continue")
                clear_console()
                return

            if approval_status == 0:
                print("Account hasn't been confirmed by the Admin")
                input("Press enter to continue")
            else:
                key = 1

        elif option == FORGOT_PASS:
            if User_service.forgot_password():
                User_service.login()

        elif option == EXIT:
            clear_console()
            return

        if key:
            clear_console()
            print(f"Welcome {User_service.registered_user.name}")
            handle_account_option()
        
        clear_console()
