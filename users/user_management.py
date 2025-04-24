import json
from account import handle_account_option
from utils import clear_console
import random

class User:
    def __init__(self, username: str, pin: str):
        self.username = username
        self.pin = pin
        self.balance = 0.0
        
        self.account_number = None  # Placeholder for account number
        self.account_type = None  # Placeholder for account type
        self.account_status = None  # Placeholder for account status
        self.account_creation_date = None  # Placeholder for account creation date
        self.account_last_transaction_date = None  # Placeholder for last transaction date

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        user = User(data['username'], data['pin'])
        user.balance = data.get('balance', 0.0)
        user.account_number = data.get('account_number')
        user.account_type = data.get('account_type')
        user.account_status = data.get('account_status')
        user.account_creation_date = data.get('account_creation_date')
        user.account_last_transaction_date = data.get('account_last_transaction_date')
        return user


class UserService:
    current_user: User | None = None
    users = []  # List to store registered users
    users_file = "users.json"

    def __init__(self):
        self.load_users()

    def save_users(self):
        try:
            with open(self.users_file, 'w') as file:
                json.dump([user.to_dict() for user in self.users], file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving users: {e}")

    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                users_data = json.load(file)
                self.users = [User.from_dict(user_data) for user_data in users_data]
        except FileNotFoundError:
            self.users = []  # Initialize with an empty list if file doesn't exist
        except Exception as e:
            print(f"An error occurred while loading users: {e}")

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
            print("=== Welcome to Account Registration ===")
            
            # Accept Terms and Conditions
            print("\n=== Terms and Conditions ===")
            print("By registering, you agree to the terms and conditions of our banking services.")
            accept_terms = input("Do you accept the terms and conditions? (yes/no): ").strip().lower()
            if accept_terms != "yes":
                print("You must accept the terms and conditions to proceed. Returning to the main menu.")
                return

            print("Please select the type of account you want to open:")
            print("1. Individual Account")
            print("2. Business Account")
            account_type_choice = input("Enter your choice (1 or 2): ")

            if account_type_choice not in ["1", "2"]:
                print("Invalid choice. Registration failed.")
                return

            account_type = "Individual" if account_type_choice == "1" else "Business"

            if account_type == "Individual":
                print("\n=== A. PERSONAL INFORMATION ===")
                full_name = input("Enter your full name (Last Name, First Name Middle Name): ")
                date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
                contact_number = input("Enter your contact number: ")
                email = input("Enter your email address: ")
                address = input("Enter your address: ")

                print("\n=== B. ACCOUNT INFORMATION ===")
                id_type = input("Enter the type of ID (e.g., Passport, Driver's License): ")
                id_number = input("Enter your ID number: ")
                tin = input("Enter your TIN (if applicable, N/A if none): ")

                print("\n=== C. ACCOUNT PREFERENCE ===")
                account_preference = input("Enter your account preference (Savings Account or Checking Account): ")

            else:  # Business Account
                print("\n=== A. BUSINESS INFORMATION ===")
                business_name = input("Enter your business name: ")
                business_registration_number = input("Enter your business registration number: ")
                contact_number = input("Enter your business contact number: ")
                email = input("Enter your business email address: ")
                address = input("Enter your business address: ")

                print("\n=== B. ACCOUNT INFORMATION ===")
                id_type = input("Enter the type of ID (e.g., Business Permit, Tax ID): ")
                id_number = input("Enter your ID number: ")
                tin = input("Enter your TIN (if applicable, leave blank if none): ")

                print("\n=== C. ACCOUNT PREFERENCE ===")
                account_preference = input("Enter your account preference (Savings Account or Checking Account): ")

            print("\n=== D. SECURITY INFORMATION ===")
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            confirm_password = input("Confirm your password: ")

            if password != confirm_password:
                print("Passwords do not match. Registration failed.")
                return

            for user in self.users:
                if user.username == username:
                    print("Username already exists. Please choose a different username.")
                    return

            # Generate a unique 11-digit account number
            account_number = str(random.randint(10**10, 10**11 - 1))

            # Create the new user
            new_user = User(username, password)
            new_user.account_type = account_type
            new_user.account_number = account_number
            new_user.balance = 0.0  # Initial balance
            new_user.account_status = "Active"

            # Add additional fields based on account type
            if account_type == "Individual":
                new_user.full_name = full_name
                new_user.date_of_birth = date_of_birth
                new_user.contact_number = contact_number
                new_user.email = email
                new_user.address = address
                new_user.id_type = id_type
                new_user.id_number = id_number
                new_user.tin = tin
                new_user.account_preference = account_preference
            else:  # Business Account
                new_user.business_name = business_name
                new_user.business_registration_number = business_registration_number
                new_user.contact_number = contact_number
                new_user.email = email
                new_user.address = address
                new_user.id_type = id_type
                new_user.id_number = id_number
                new_user.tin = tin
                new_user.account_preference = account_preference

            self.users.append(new_user)
            self.save_users()  # Save the new user to the JSON file
            self.current_user = new_user

            # Display success
            print("Registration successful! Your account has been created.")
        except Exception as e:
            print(f"An error occurred during registration: {e}")
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
            self.save_users()  # Save the updated PIN to the JSON file
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
            self.save_users()  # Save the updated username to the JSON file
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