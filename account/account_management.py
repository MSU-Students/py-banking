from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
from datetime import datetime

class AccountService:
    current_account: BankAccount | None = None
    accounts: List[BankAccount] = list()   

    def create_account(self):
        print("\nWelcome to PY Banking!")
        print("Let's create your new bank account.")
        while True:
            last_name = input("Enter account holder's last name: ").strip()
            first_name = input("Enter account holder's first name: ").strip()
            middle_name = input("Enter account holder's middle name: ").strip()
            
            if not last_name.isalpha():
                print("Last name must contain only alphabetic characters. Please try again.")
                continue
            if not first_name.isalpha():
                print("First name must contain only alphabetic characters. Please try again.")
                continue
            if not middle_name.isalpha():
                print("Middle name must contain only alphabetic characters. Please try again.")
                continue
            
            account_name = f"{last_name}, {first_name} {middle_name}"
            break
        
        # Generate account ID in the format YYYYMMDDXXXX (e.g., 202310150001)
        date_part = datetime.now().strftime("%Y%m%d")
        unique_part = f"{len(self.accounts) + 1:04d}"  # Ensure 4-digit unique part
        account_id = f"{date_part}{unique_part}"
        
        while True:
            try:
                initial_balance = float(input("Enter initial deposit amount: "))
                if initial_balance < 0:
                    print("Initial deposit amount cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Initial deposit amount must be a valid number. Please try again.")
        # Create a new BankAccount instance
        new_account = BankAccount(account_id, account_name, initial_balance)
        
        # Set the new account as the current account
        self.current_account = new_account
        
        # Add the new account to the accounts list
        self.accounts.append(new_account)
        
        print(f"Account created successfully for {account_name} with ID {account_id}.")
    
    def select_account(self):
        if not self.accounts:
            print("No accounts available to select.")
            return
        
        print("\nAvailable Accounts:")
        for account in self.accounts:
            print(f"ID: {account.user_id}, Name: {account.account_name}")
        
        while True:
            try:
                user_id = input("Enter the ID of the account to select: ").strip()
                selected_account = self.find_account(user_id)
                if selected_account:
                    self.current_account = selected_account
                    print(f"Account with ID {user_id} selected successfully.")
                    break
                else:
                    print("Account not found. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid account ID.")
    
    def find_account(self, id: str) -> BankAccount | None:
        for account in self.accounts:
            if account.user_id == id:
                return account
        return None

    def balance_inquiry(self):
        if self.current_account:
            print(f"Account Balance for {self.current_account.account_name}: {self.current_account.balance:.2f}")
        else:
            print("No account selected. Please select an account first.")

    def delete_account(self):
        if not self.accounts:
            print("No accounts available to delete.")
            return
        
        print("\nAvailable Accounts:")
        for account in self.accounts:
            print(f"ID: {account.user_id}, Name: {account.account_name}")
        
        while True:
            try:
                user_id = input("Enter the ID of the account to delete: ").strip()
                selected_account = self.find_account(user_id)
                if selected_account:
                    self.accounts.remove(selected_account)
                    if self.current_account == selected_account:
                        self.current_account = None
                    print(f"Account with ID {user_id} deleted successfully.")
                    break
                else:
                    print("Account not found. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid account ID.")

account_service = AccountService()

EXIT, WITHDRAW, DEPOSIT, BALANCE, SELECT, SERVICES, TRANSACTION = (0, 1, 2, 3, 4, 5, 6)
'''
Main Account Menu
'''
def print_account_menu():
    print("Bank Account Options:")
    print(f"\t{WITHDRAW} : Withdraw")
    print(f"\t{DEPOSIT} : Deposit")
    print(f"\t{BALANCE} : Balance")
    print(f"\t{SELECT} : Select Other Account")
    print(f"\t{SERVICES} : Services")
    print(f"\t{TRANSACTION} : View Transaction History")
    #other options here
    print(f"\t{EXIT} : Exit")

CREATE_ACCOUNT, LOAN = (1, 2)
'''
Main Account Sub Menu: Services 
'''
def print_services_options():
    print('Services Options:')
    print(f"\t{CREATE_ACCOUNT} : CREATE NEW ACCOUNT")
    print(f"\t{LOAN} : LOAN SERVICES")
    #other options here
    print(f"\t{EXIT} : Exit")


def handle_services_option():
    option = CREATE_ACCOUNT 
    while option != EXIT:
        print_services_options()
        option = int(input("\n\tCommand: "))
        if option == CREATE_ACCOUNT:
            account_service.create_account()
        elif option == LOAN:
            # clear_console()
            handle_loan_option(account_service.current_account)
            # handle other options here
            # clear_console()
        print("Exiting account options...")


def handle_account_option():
    option = SERVICES
    transaction_service: TransactionService
    if len(account_service.accounts) == 0:
        account_service.create_account()
        
    while option != EXIT and account_service.current_account != None:
        transaction_service = TransactionService(account_service.current_account)
        print_account_menu()
        try:
            option = int(input("\n\tCommand: "))
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the menu options.")
            continue
        if option == SERVICES:
            # clear_console()
            handle_services_option()
        elif option == SELECT:
            account_service.select_account()
        elif option == WITHDRAW:
            amount = float(input("Enter withdrawal amount: "))
            transaction_service.withdrawal(amount)
        # deposit
        elif option == DEPOSIT:
            amount = float(input("Enter deposit amount: "))
            transaction_service.deposit(amount)
        # view transaction history
        elif option == TRANSACTION:  
            transaction_service.display_transactions()
                                        
             
        elif option == BALANCE:
            transaction_service.balance_inquiry()
        # clear_console()

