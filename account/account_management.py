from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
from random import random
class AccountService: #kurt
    current_account: BankAccount | None = None
    accounts:List[BankAccount] = list()
    current_user = None
    
    def create_account(self):
        input("TODO:create account okay?:") #dito mag stop
        #replace the following temporary code
        account_name = 'Dummy' #TODO: replace this code
        account_num = str(int(999999 * random()))
        print("Account Create:", account_num)
        self.current_account = BankAccount(self.current_user.User_Id, account_name, account_num, 500)
        self.accounts.append(self.current_account)
        input("Press enter to continue")
    
    def select_account(self):
        input("TODO:list account and select")
        
    def find_account(self, id: int) -> BankAccount|None:
        print("TODO:find account:", id)
        return None
    def find_account_by_number(self, num : str) -> BankAccount|None:
        for account in self.accounts:
            if num == account.account_number:
                return account
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

CREATE_ACCOUNT, LOAN, FUND_TRANSFER = (1, 2, 3)
'''
Main Account Sub Menu: Services
'''
def print_services_options():
    print('Services Options:')
    print(f"\t{CREATE_ACCOUNT} : CREATE NEW ACCOUNT")
    print(f"\t{LOAN} : LOAN SERVICES")
    print(f"\t{FUND_TRANSFER} : FUND TRANSFER")
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
        elif option == FUND_TRANSFER:
            clear_console()
            process_fund_transfer()
        # handle other options here
        clear_console()
def process_fund_transfer(): 
    account_num = input("Enter target account number:")
    amount = float(input("Enter amount to transfer:"))
    transaction_service = TransactionService(account_service.current_account)
    target_account = account_service.find_account_by_number(account_num)
    if target_account != None:
        transaction_service.transfer_fund(target_account, amount)

def handle_account_option(user): #group 1
    option = SERVICES
    account_service.current_user = user
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