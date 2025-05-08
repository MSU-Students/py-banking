from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import random
import json

SAVINGS, CHECKING = (1,2)
class AccountService: #kurt
    current_account: BankAccount | None = None
    accounts:List[BankAccount] = list()   

    def create_account(self):

        print("Create an Account: ") 
        print("What type of account will you open? Choose Below")
        print("1. Savings\n2. Checking")
        account_type=(input("Decision: "))
        if account_type == SAVINGS:
            self.current_account.account_number(str(random.randint(10000, 99999)))
            self.current_account.balance(input("Deposit min of Php 500 for maintaining balance: "))
                            
        elif account_type == CHECKING:
            self.current_account.account_number(str(random.randint(10000, 99999)))
            self.current_account.balance(input("Deposit min of Php 500 for maintaining balance: "))
                   
        account_data = {
            "user_id": self.current_account.user_id(),
            "account_type":self.current_account.account_type(),
            "account_number": self.current_account.account_number(),
            "balance":self.current_account.balance()
        }
       
        self.current_account = BankAccount()
        self.accounts.append(account_data)
        with open("accounts.json", 'w') as account:
            json.dump(self.accounts, account, indent=4)
        self.current_account = BankAccount(self.current_account.user_id,self.current_account.account_type,self.current_account.account_number,self.current_account.account_balance)
        print(f'Congratulations! You have successfully registered a {self.current_account.account_type} account!')
        print(f'Information:\nUser_id: {self.current_account.user_id}')
        print(f'Account Type: {self.current_account.account_type}')
        print(f'Account Number: {self.current_account.account_number}')
        print(f'Account Balance: {self.current_account.account_balance}')
        return
    
    def select_account(self):
        input("TODO:list account and select")
        
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
    transaction_service: TransactionService
    if len(account_service.accounts) == 0:
        account_service.create_account()
        
    while option != EXIT and account_service.current_account != None:
        transaction_service = TransactionService(account_service.current_account)
        print_account_menu()
        option = int(input("\n\tCommand: "))
        if option == SERVICES:
            clear_console()
            handle_services_option()
        elif option == SELECT:
            account_service.select_account()
        elif option == WITHDRAW:
            transaction_service.withdrawal()
        # handle other options here
        clear_console()