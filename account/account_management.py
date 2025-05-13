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
    accounts: List[BankAccount] = list()
    # user_accounts: List[BankAccount] = list()
    accounts_file = "accounts.json"
    current_account: List
    #delete if nag error ang create acc
    accounts_data = []
    transaction : List[TransactionService] = list()
    
    def __init__(self, user_id: str = "", account_type: str = "", account_number: str = "", account_balance: float = 0.0):
        
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r') as file:
                self.accounts_data = json.load(file)
        else:
            self.accounts_data = []
            
        self.user_id = user_id
        self.account_type = account_type
        self.account_number = account_number
        self.account_balance = account_balance

    def user_has_account(self, user_id: str) -> bool:
        for account in self.accounts_data:
            if account["user_id: "]== user_id:
                return True
            else:
                print("nalyn error")
        return False

    def create_account(self, user_id: str = None):
        print("Create an Account: ")
        print("What type of account will you open? Choose Below")
        print("1. Savings\n2. Checking")
        option = input("Decision: ")

        if user_id is None:
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
            try:
                initial_balance = float(input("Enter initial deposit amount: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                attempts += 1
                continue

            if initial_balance >= 500:
                self.current_account = BankAccount(user_id=user_id, account_number=account_number, account_type=account_type, account_balance=initial_balance)

                account_data = {
                    "user_id: ": self.current_account.user_id,
                    "account_type: ": self.current_account.account_type,
                    "account_number: ": self.current_account.account_number,
                    "account_balance: ": self.current_account.account_balance,
                }
                self.accounts_data.append(account_data)

                with open(self.accounts_file, 'w') as account_file:
                    json.dump(self.accounts_data, account_file, indent=4)
                
                
                print(f'Information:\nUser_id: {self.current_account.user_id}')
                print(f'Account Type: {self.current_account.account_type}')
                print(f'Account Number: {self.current_account.account_number}')
                print(f'Account Balance: {self.current_account.account_balance}')
                os.system("pause")
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



    def select_account(self, user_id: str):
        self.user_accounts = []
        # accounts_data : a variable that has all the  important details of the user's accounts
        for user in self.accounts_data: 
            # if ang user_id na ininput ng user galing sa log_in mah equal sa accounts.json na user_id, i-initialize and store niya yung mga variables na dictionary dito sa bank account class
            if user["user_id: "] == user_id:
                account = BankAccount(
                    user_id=user["user_id: "],
                    account_type=user["account_type: "],
                    account_number=user["account_number: "],
                    account_balance=user["account_balance: "]
                )
      
                # user_accounts = [] - a python list 
                self.user_accounts.append(account)
            
        if not self.user_accounts:
            print('You do not have any existing account!')
            return False
        
    # LIST UR ACCOUNTS
        print("List of Account You Have:")
        index = 0
        for account in self.user_accounts:
            print(f"{index+1}.\tAccount Type: {account.account_type}\n\tAccount Number: {account.account_number}\n\tAccount Balance: {account.account_balance}")
            index +=1
    #  CHECK IF THE NUMBER U SELECTED IS EQUAL SA INDEX NG USER_ACCOUNTS  
        selected_index = int(input("Select account: "))
        for account_details in self.user_accounts:
            if 1 <= selected_index <=(len(self.user_accounts)+1):
                selected_account = self.user_accounts[selected_index-1]
            return selected_account  
        else:
            print('mali nalyn, wala nakita ang account, mali guro ka sa index')

                
        
        

    def find_account(self, id: int) -> BankAccount | None:
        print("TODO:find account:", id)
        return None
    # TODO: Other methods such as (balance_inquiry)

account_service = AccountService()
transaction_data = []

EXIT, WITHDRAW, DEPOSIT, BALANCE, TRANSACTION_HISTORY, SELECT, SERVICES = (0, 1, 2, 3, 4, 5,6)

'''
Main Account Menu
'''
def print_account_menu():
    print("Bank Account Options:")
    print(f"\t{WITHDRAW} : Withdraw")
    print(f"\t{DEPOSIT} : Deposit")
    print(f"\t{BALANCE} : Balance")
    print(f"\t{TRANSACTION_HISTORY}: View Transaction History") 
    print(f"\t{SELECT} : Select Other Account")
    print(f"\t{SERVICES} : Services")
    # other options here
    print(f"\t{EXIT} : Exit")

CREATE_ACCOUNT, LOAN = (1, 2)

'''
Main Account Sub Menu: Services
'''
def print_services_options():
    print('Services Options:')
    print(f"\t{CREATE_ACCOUNT} : CREATE NEW ACCOUNT")
    print(f"\t{LOAN} : LOAN SERVICES")
    # other options here
    print(f"\t{EXIT} : Exit")

def handle_services_option():
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
        # handle other options here
        clear_console()

def handle_account_option(user_id: str):
    option = SERVICES
    if not account_service.user_has_account(user_id):
        print("No account found. Please create an account.")
        account_service.create_account(user_id)

    while option != EXIT:
        print_account_menu()
        try:
            option = int(input("\n\tCommand: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == SERVICES:
            clear_console()
            handle_services_option()
        elif option == SELECT:
            account_service.select_account(user_id)
        #ALI -WITHDRAW    
        elif option == WITHDRAW:
            print(f'__'*20)
            print("\n\tSelect an Account to Withdraw")
            print(f'__'*20)
            #selcted_Account : this is the account selected by the user on select_account function
            selected_account = account_service.select_account(user_id)
            account_type = selected_account.account_type
            account_number = selected_account.account_number
            account_balance = selected_account.account_balance
            
            if selected_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            transaction_service = TransactionService(account=selected_account)
            try:
                amount = float(input("\nEnter amount to withdraw: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            transaction_service.withdrawal(amount, user_id,account_type, account_number, account_balance)
        #THAMEENAH -DEPOSIT
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu
        elif option == DEPOSIT:
             #selcted_Account : this is the account selected by the user on select_account function
            print(f'__'*20)
            print("\n\tSelect an Account to Deposit")
            print(f'__'*20)
            selected_account = account_service.select_account(user_id)
            account_type = selected_account.account_type
            account_number = selected_account.account_number
            account_balance = selected_account.account_balance
            
            if selected_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            transaction_service = TransactionService(account=selected_account)
            try:
                amount = float(input("\nEnter amount to deposit: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
           
            transaction_service.deposit(amount, user_id,account_type, account_number, account_balance)
            
        #NORHAILAH   - balance inquiry
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu 
        elif option == BALANCE:
            
            print(f'__'*20)
            print("\n\tSelect an Account to Inquire Balance")
            print(f'__'*20)
             #selcted_Account : this is the account selected by the user on select_account function
            selected_account = account_service.select_account(user_id)
            account_type = selected_account.account_type
            account_number = selected_account.account_number
            account_balance = selected_account.account_balance
            
            if selected_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
          
            
            transaction_service = TransactionService(account=selected_account)
            print(f"Account Balance: {selected_account.account_balance}")
            transaction_service.balance_inquiry(user_id,account_type, account_number, account_balance)
            
        elif option == TRANSACTION_HISTORY:
            print(f'__'*20)
            print("\n\tSelect an Account to View Transaction History")
            print(f'__'*20)
             #selcted_Account : this is the account selected by the user on select_account function
            selected_account = account_service.select_account(user_id)
            account_type = selected_account.account_type
            account_number = selected_account.account_number
            account_balance = selected_account.account_balance
            
            if selected_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
          
            transaction_service = TransactionService(account=selected_account)
            transaction_service.display_transactions(user_id,account_type, account_number, account_balance)
            
        elif option == EXIT:
            clear_console()
            return