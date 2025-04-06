from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService

class AccountService:
    current_account: BankAccount | None = None
    accounts:List[BankAccount] = list()   

    def create_account(self):
        input("TODO:create account:")
        #replace the following temporary code
        self.current_account = BankAccount();
        self.accounts.append(self.current_account)
    
    def select_account(self):
        input("TODO:list account and select") 
        
    def find_account(self, id: int) -> BankAccount|None:
        print("TODO:find account:", id) 
        return None
    # Other methods here

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


def handle_account_option():
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

