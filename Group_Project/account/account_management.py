from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import random
import string

class AccountService: #kurt
    current_account: BankAccount | None = None
    accounts:List[BankAccount] = list()   

    def create_account(self):
        self.current_account = BankAccount()
        self.accounts.append(self.current_account)
    
    def select_account(self):
        input("TODO:list account and select")
        
    def find_account(self, id: int) -> BankAccount|None:
        print("TODO:find account:", id)
        return None
    #TODO: Other methods such as (balance_inquery)
    
    #User Authentication
def User_Authentication(length=4):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def changepassword_menu():

    print("===============================")
    print("         CHANGE PIN")
    print("===============================")

    entered_pin = input("Enter your previous PIN: ")

    if entered_pin != pin:
        print("Incorrect previous PIN.")
        return

    new_pin = input("Enter new PIN (4 digits only): ")
    if not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must be exactly 4 digits.")
        return

    confirm_pin = input("Re-enter your new PIN: ")
    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    code = str(random.randint(100000, 999999))
    print(f"\nCode: Type the characters shown below:\n[ {code} ]")
    entered_code = input("Enter the code: ")

    if entered_code != code:
        print("Incorrect code.")
        return

    #If sumakses edi change [pin]
    pin = new_pin


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


def handle_services_option():
    option = CREATE_ACCOUNT 
    while option != EXIT:
        print_services_options()
        option = int(input("\n\tCommand: "))
        if option == CREATE_ACCOUNT:
            print(f"\t{EXIT} : Exit")
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