from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import random
import json
import os




SAVINGS, CHECKING = (1,2)
class AccountService: #kurt
    user_id: str
    account_type: str
    account_number: str
    account_balance: float
    accounts:List[BankAccount] = list()
    
    accounts_file = "accounts.json"
    current_account:List

    def __init__(self):
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r') as file:
                self.accounts_data = json.load(file)
        else:
            self.accounts_data = []
            
    def create_account(self):
        print("Create an Account: ") 
        print("What type of account will you open? Choose Below")
        print("1. Savings\n2. Checking")
        option = input("Decision: ")
        
        user_id = input("Enter your User ID: ")
        if option == str(SAVINGS):
            account_type = "savings"
        elif option == str(CHECKING):
            account_type = "checking"
        else:
            print("Invalid option. Please select 1 for Savings or 2 for Checking.")
            return
            
        account_number = str(random.randint(10000, 99999))
        attempts = 0
        while attempts < 3:
            initial_balance = float(input("Enter initial deposit amount: "))
            if initial_balance >= 500:
                self.current_account = BankAccount(user_id="", account_number="", account_type="", account_balance=0.0)
                self.current_account.user_id = user_id
            
                account_data = {
                    "user_id": self.current_account.user_id,
                    "account_type": self.current_account.account_type,
                    "account_number": self.current_account.account_number,
                    "balance": self.current_account.account_balance,
                }
                self.accounts_data.append(account_data)
                
                with open("accounts.json", 'w') as account:
                    json.dump(self.accounts_data, account, indent=4)
                
                print(f'Information:\nUser_id: {self.current_account.user_id}')
                print(f'Account Type: {self.current_account.account_type}')
                print(f'Account Number: {self.current_account.account_number}')
                print(f'Account Balance: {self.current_account.account_balance}')
                break
            else:
                print("Error: Minimum deposit is Php 500.")
                attempts += 1
                if attempts < 3:
                    print("Please try again.")
                else:
                    print("Maximum attempts reached. Exiting.")
                    clear_console()
                    return 
            
        

    def new_method(self):
        return
    
    def select_account(self):
        for item, account in enumerate(account_service.accounts_data):
            print(f"{item + 1}. Account Number: {account['account_number']}, Type: {account['account_type']}, Balance: {account['balance']}")
        
        selected_index = int(input("Enter the number of the account: ")) - 1
        return selected_index
            
        
    def find_account(self, id: int) -> BankAccount|None:
        print("TODO:find account:", id)
        return None
    #TODO: Other methods such as (balance_inquery)

account_service = AccountService()

EXIT, WITHDRAW, DEPOSIT, BALANCE, SELECT, SERVICES = (0, 1, 2, 3, 4, 5)
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
            clear_console()
            handle_loan_option(account_service.current_account)
        # handle other options here
        clear_console()


def handle_account_option(): #group 1
    option = SERVICES
    if len(account_service.accounts_data) == 0:
        print("No account found. Please create an account.")
        account_service.create_account()
    
    while option != EXIT:
        print_account_menu()
        option = int(input("\n\tCommand: "))
        if option == SERVICES:
            clear_console()
            handle_services_option()
        elif option == SELECT:
            account_service.select_account()
            
            
        elif option == WITHDRAW:
            print("\t\WITHDRAW\nSelect an account to withdraw into:")
            for item, account in enumerate(account_service.accounts_data):
                print(f"{item + 1}. Account Number: {account['account_number']}, Type: {account['account_type']}")
            
            selected_index = int(input("Enter the number of the account: ")) - 1
            if selected_index < 0 or selected_index >= len(account_service.accounts_data):
                print("Invalid selection. Please try again.")
                continue
            
            selected_account = account_service.accounts_data[selected_index]
            transaction_service = TransactionService(account=selected_account)
            amount = float(input("\nEnter ammount to withdraw: "))
            transaction_service.withdrawal(amount)
            
                
                
        elif option == DEPOSIT:
            print("\t\tDEPOSIT\nSelect an account to deposit into:")
            for item, account in enumerate(account_service.accounts_data):
                print(f"{item + 1}. Account Number: {account['account_number']}, Type: {account['account_type']}")
            
            selected_index = int(input("Enter the number of the account: ")) - 1
            if selected_index < 0 or selected_index >= len(account_service.accounts_data):
                print("Invalid selection. Please try again.")
                continue
            
            selected_account = account_service.accounts_data[selected_index]
            transaction_service = TransactionService(account=selected_account)
            amount = float(input("\nEnter deposit amount: "))
            transaction_service.deposit(amount)
            
        elif option == BALANCE:
            print("\t\Balance\nSelect an account to check balance:")
            for item, account in enumerate(account_service.accounts_data):
                print(f"{item + 1}. Account Number: {account['account_number']}, Type: {account['account_type']}")
            
            selected_index = int(input("Enter the number of the account: ")) - 1
            if selected_index < 0 or selected_index >= len(account_service.accounts_data):
                print("Invalid selection. Please try again.")
                continue
            selected_account = account_service.accounts_data[selected_index]
            transaction_service = TransactionService(account=selected_account)
            transaction_service.balance_inquiry()
        elif option == EXIT:
            clear_console()
            return
            
    
     
     