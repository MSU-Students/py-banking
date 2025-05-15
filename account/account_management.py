from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import json
import os

class AccountService:
    current_account: BankAccount | None = None
    accounts: List[BankAccount] = list()

    def __init__(self):
        self.accounts_file = "accounts.json"  
        self.accounts = self.load_accounts()  

    def load_accounts(self): 
        if not os.path.exists(self.accounts_file):
            return []
        
        with open(self.accounts_file, "r") as f:
            data = json.load(f)
            return [BankAccount.from_dict(acc) for acc in data]

    def save_accounts(self): 
        with open(self.accounts_file, "w") as f:
            json.dump([acc.to_dict() for acc in self.accounts], f, indent=4)

    def create_account(self): 
        from users.user_management import User_service
        try:
            balance = float(input("Enter initial deposit amount: "))
        except ValueError: 
            print("Invalid input for balance.")
            return

        new_account = BankAccount(User_service.login_user.User_Id,User_service.login_user.name, balance)
        self.accounts.append(new_account)
        self.current_account = new_account
        self.save_accounts()

        print(f"\nAccount created successfully for {new_account.full_name}!")
        print(f"Account ID: {new_account.account_id}")
        print(f"Balance: ₱{new_account.balance:.2f}\n")


    def list_accounts(self):
        from users.user_management import User_service
        user_id = User_service.login_user.User_Id
        user_accounts = [acc for acc in self.accounts if acc.user_id == user_id]

        if not user_accounts:
            print("No accounts found for this user.\n")
            return []

        print("\nYour Accounts:")
        for i, acc in enumerate(user_accounts, start=1):
            print(f"{i}. {acc.full_name} - Account ID: {acc.account_id} - Balance: ₱{acc.balance:.2f}")
        return user_accounts


    def select_account(self):
        user_accounts = self.list_accounts()
        if not user_accounts:
            return

        try:
            choice = int(input("\nEnter the number of the account to select: "))
            if 1 <= choice <= len(user_accounts):
                self.current_account = user_accounts[choice - 1]
                print(f"\nSelected account: {self.current_account.full_name} - Balance: ₱{self.current_account.balance:.2f}\n")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")


    def find_account(self, id: int) -> BankAccount | None:
        #Find account by account ID
        for acc in self.accounts:
            if acc.account_id == id:
                return acc
        return None



account_service = AccountService()
transaction_data = []

EXIT, WITHDRAW, DEPOSIT, BALANCE, TRANSACTION_HISTORY, SELECT, SERVICES = (0, 1, 2, 3, 4, 5,6)

EXIT, WITHDRAW, DEPOSIT, BALANCE, SELECT, SERVICES = (0, 1, 2, 3, 4, 5)

def print_account_menu():
    #Print main account options
    print("Bank Account Options:")
    print(f"\t{WITHDRAW} : Withdraw")
    print(f"\t{DEPOSIT} : Deposit")
    print(f"\t{BALANCE} : Balance Inquiry")
    print(f"\t{SELECT} : Select Another Account")
    print(f"\t{SERVICES} : Access Services")
    print(f"\t{EXIT} : Exit")

CREATE_ACCOUNT, LOAN, CHANGE_INFO, CHANGE_PASS = (1, 2, 3, 4)

def print_services_options():
    #Print options for services menu
    print('Services Options:')
    print(f"\t{CREATE_ACCOUNT} : CREATE NEW ACCOUNT")
    print(f"\t{LOAN} : LOAN SERVICES")
    print(f"\t{CHANGE_INFO} : CHANGE PROFILE INFORMATION")      
    print(f"\t{CHANGE_PASS} : CHANGE PASSWORD")    
    print(f"\t{EXIT} : Exit")

def handle_services_option():
    #Handle user services options
    from users.user_management import User_service
    option = CREATE_ACCOUNT 
    while option != EXIT:
        print_services_options()
        try:
            option = int(input("\n\tCommand: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if option == CREATE_ACCOUNT:
            account_service.create_account()
        elif option == LOAN:
            clear_console()
            handle_loan_option(account_service.current_account)
        elif option == CHANGE_INFO:
            clear_console()
            User_service.change_info()
        elif option == CHANGE_PASS:
            clear_console()
            User_service.change_pass()
        clear_console()
def process_fund_transfer(): 
    account_num = input("Enter target account number:")
    amount = float(input("Enter amount to transfer:"))
    transaction_service = TransactionService(account_service.current_account)
    target_account = account_service.find_account_by_number(account_num)
    if target_account != None:
        transaction_service.transfer_fund(target_account, amount)

LOGIN, CREATE = (1, 2)

def login_account_menu():
    #Allow the user to log in or create a new account
    print("Choose an option")
    print(f"\t{LOGIN} : LOGIN ACCOUNT")
    print(f"\t{CREATE} : CREATE ACCOUNT")
    print(f"\t{EXIT} : EXIT")
    choice = int(input("CHOICE: "))

    if choice == LOGIN:
        account_service.select_account()
    elif choice == CREATE:
        account_service.create_account()
    else:
        return

def handle_account_option():
    #Handle the account options menu and perform related actions
    option = SERVICES
    transaction_service: TransactionService
    login_account_menu()

    while option != EXIT and account_service.current_account != None:
        transaction_service = TransactionService(account_service.current_account)
        print_account_menu()
        option = int(input("\n\tCommand: "))
        if option == SERVICES:
            clear_console()
            handle_services_option()
        elif option == SELECT:
            account_service.select_account()
        #ALI -WITHDRAW    
        elif option == WITHDRAW:
            transaction_service.withdrawal()
        # handle other options here
        clear_console()
