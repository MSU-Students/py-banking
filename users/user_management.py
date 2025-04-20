from account import handle_account_option
from utils import clear_console
class User:
    def __init__(self, username: str, pin: str):
        self.username = username
        self.pin = pin
        self.balance = 0.0
        self.account_number = None # Placeholder for account number
        self.account_type = None # Placeholder for account type
        self.account_status = None # Placeholder for account status
        self.account_creation_date = None # Placeholder for account creation date
        self.account_last_transaction_date = None # Placeholder for last transaction date       
    
class UserService:
    current_user: User | None = None
    users = []  # List to store registered users

    def login(self):
        try:
            username = input("Enter your username: ")
            pin = input("Enter your PIN: ")
            for user in self.users:
                if user.username == username and user.pin == pin:
                    self.current_user = user
                    print("Login successful!")
                    return
            print("Invalid username or PIN. Please try again.")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    def register(self):
        try:
            username = input("Enter a username: ")
            pin = input("Enter a PIN: ")
            confirm_pin = input("Confirm your PIN: ")
            if pin != confirm_pin:
                print("PINs do not match. Registration failed.")
                return
            for user in self.users:
                if user.username == username:
                    print("Username already exists. Please choose a different username.")
                    return
            new_user = User(username, pin)
            self.users.append(new_user)
            self.current_user = new_user
            print("Registration successful!")
        except Exception as e:
            print(f"An error occurred during registration: {e}")

    def change_pin(self):
        try:
            if self.current_user is None:
                print("No user is currently logged in.")
                return
            current_pin = input("Enter your current PIN: ")
            if self.current_user.pin != current_pin:
                print("Incorrect current PIN.")
                return
            new_pin = input("Enter a new PIN: ")
            confirm_new_pin = input("Confirm your new PIN: ")
            if new_pin != confirm_new_pin:
                print("PINs do not match. PIN change failed.")
                return
            self.current_user.pin = new_pin
            print("PIN changed successfully!")
        except Exception as e:
            print(f"An error occurred while changing the PIN: {e}")

    def update_profile(self):
        try:
            if self.current_user is None:
                print("No user is currently logged in.")
                return
            new_username = input("Enter a new username: ")
            for user in self.users:
                if user.username == new_username:
                    print("Username already exists. Please choose a different username.")
                    return
            self.current_user.username = new_username
            print("Profile updated successfully!")
        except Exception as e:
            print(f"An error occurred while updating the profile: {e}")

user_service = UserService()

EXIT, LOGIN, REGISTER, ADMIN_LOGIN = (0, 1, 2, 3)

def print_main_menu():
    print("Options:")
    print(f"\t{LOGIN} : Login")
    print(f"\t{REGISTER} : Register")
    print(f"\t{ADMIN_LOGIN} : Admin Login")
    print(f"\t{EXIT} : Exit")

def handle_admin_login():
    admin_username = "admin"
    admin_password = "admin123"
    try:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if username == admin_username and password == admin_password:
            print("Admin login successful!")
            # Add admin-specific functionality here
        else:
            print("Invalid admin credentials.")
    except Exception as e:
        print(f"An error occurred during admin login: {e}")

def handle_user_option():
    option = LOGIN
    while option != EXIT:
        print_main_menu()
        option = int(input("\n\tCommand: "))
        if option == LOGIN:
            user_service.login()
        elif option == REGISTER:
            user_service.register()
        elif option == ADMIN_LOGIN:
            handle_admin_login()
        elif option == EXIT:
            clear_console()
            return
        if user_service.current_user is not None:
            input("Press Enter to continue...")  # Pause to allow the success message to be seen
            clear_console()
            handle_account_option()
        
        clear_console()