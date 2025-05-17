from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import json
import os
import random
from datetime import datetime

SAVINGS, CHECKING =(1,2)
class AccountService:
    current_account: BankAccount | None = None
    accounts: List[BankAccount] = list()

    def __init__(self):
        self.accounts_file = "data/accounts.json"  
        self.accounts = self.load_accounts()  

    def load_accounts(self): 
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'w') as file:
                file.write('[]')
            return []
        
        with open(self.accounts_file, "r") as f:
            data = json.load(f)
            return [BankAccount.from_dict(acc) for acc in data]

    def save_accounts(self): 
        with open(self.accounts_file, "w") as f:
            json.dump([acc.to_dict() for acc in self.accounts], f, indent=4)
    
    def create_account(self, full_name, user_id): 
        clear_console()
        print("Create an Account: \n")
        print("What type of account will you open? Choose Below")
        print("1. Savings\n2. Checking")
        option = input("\nDecision: ")

        if user_id is None:
            user_id = input("Enter your User ID: ")

        #account type
        if option == str(SAVINGS):
            account_type = "SAVINGS"
        elif option == str(CHECKING):
            account_type = "CHECKING"
        else:
            print("Invalid option. Please select 1 for Savings or 2 for Checking.")
            return
        
        #account number
        account_number = str(random.randint(10000, 99999))
        
        clear_console()
        print(f"\nCreating a {account_type} account for {full_name}\n")
        #3 trials only 
        attempts = 0
        while attempts < 3:
            try:
                initial_balance = float(input("Enter initial deposit amount: "))
            except ValueError:
                print("\n\t** Invalid amount. Please enter a number **")
                print(f"\nPlease try again.")
                os.system("pause")
                clear_console()
                attempts += 1
                continue
              

            if initial_balance >= 500:
                account_data = BankAccount(user_id=user_id, full_name=full_name, balance=initial_balance, account_number=account_number, account_type=account_type)
   
                self.accounts.append(account_data)
                self.current_account = account_data
                self.save_accounts()

                print("**" * 20)
                clear_console()
                print(f"\nSuccessfully created a {account_type} account for {full_name}! Below are your account details:\n")
                print(f'Information:\n\nUser_id: {self.current_account.user_id}')
                print(f'Account Type: {self.current_account.account_type}')
                print(f'Account Number: {self.current_account.account_number}')
                print(f'Account Balance: {self.current_account.balance}\n')
                os.system("pause")
                break
            
            else:
                print("\n\t** Error: Minimum deposit is Php 500.0 **")
                attempts += 1
                if attempts < 3:
                    print(f"\nPlease try again.")
                    os.system("pause")
                    clear_console()
                else:
                    print("Maximum attempts reached. Exiting.")
                    clear_console()
                    return

    def list_accounts(self):
        from users.user_management import User_service
        user_id = User_service.login_user.user_id
        accounts = account_service.load_accounts()
        user_accounts = [acc for acc in accounts if acc.user_id == user_id]

        if not user_accounts:
            print("No accounts found for this user.\n")
            return []

        print("\nYour Accounts:")
        for i, acc in enumerate(user_accounts, start=1):
            print(f"{i}. {acc.full_name} - Account ID: {acc.account_number} - Balance: ₱{acc.balance:.2f}")
        return user_accounts
                    
    def select_account(self):
        user_accounts = self.list_accounts()
        if not user_accounts:
            print("You do not have an existing accounts. Please create one...")
            print("Automatically signing out.....")
            os.system('pause')
            return

        try:
            choice = int(input("\nEnter the number of the account to select: "))
            for account in user_accounts:
                if 1 <= choice <= (len(user_accounts)):
                    self.current_account = user_accounts[choice - 1]
                    print(f"\nSelected account: {self.current_account.full_name} - Account Number: {self.current_account.account_number}\n{self.current_account.account_type} Account - Balance: ₱{self.current_account.balance:.2f}\n")
                    return self.current_account
                else:
                    print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
            
    def user_has_account(self, user_id: str) -> bool:
        for account in self.accounts_data:
            if account["user_id: "]== user_id:
                return True
        else:
            print("\nYou don't have any existing account yet")
            input("Press enter to continue")
            return
    

    def find_account(self, account_num) -> BankAccount | None:
        #Find account by account ID
        for acc in self.accounts:
            if acc.account_id == account_num:
                return acc
        return None



account_service = AccountService()
transaction_data = []

EXIT, WITHDRAW, DEPOSIT, BALANCE, TRANSACTION_HISTORY, SELECT, SERVICES = (0, 1, 2, 3, 4, 5, 6)

EXIT, WITHDRAW, DEPOSIT, BALANCE, VIEW_TRANSACTION_HISTORY, SELECT, SERVICES, TRANSFER_FUND, GENERATE_REPORT, FILTER_TRANSACTION_HISTORY = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

def print_account_menu():
    print("Bank Account Options:")
    print(f"\t{WITHDRAW} : Withdraw")
    print(f"\t{DEPOSIT} : Deposit")
    print(f"\t{BALANCE} : Balance Inquiry")
    print(f"\t{VIEW_TRANSACTION_HISTORY} : View Transaction History")
    print(f"\t{FILTER_TRANSACTION_HISTORY} : Filter Transaction History")  # <-- Add this line
    print(f"\t{SELECT} : Select Another Account")
    print(f"\t{TRANSFER_FUND} : Fund Transfer")
    print(f"\t{GENERATE_REPORT} : Generate Report")
    print(f"\t{SERVICES} : Access Services")
    print(f"\t{EXIT} : Exit")

CREATE_ACCOUNT, LOAN, CHANGE_INFO, CHANGE_PASS, SEE_PROFILE = (1, 2, 3, 4, 5)

def print_services_options():
    #Print options for services menu
    print('Services Options:')
    print(f"\t{CREATE_ACCOUNT} : CREATE NEW ACCOUNT")
    print(f"\t{LOAN} : LOAN SERVICES")
    print(f"\t{CHANGE_INFO} : CHANGE PROFILE INFORMATION")      
    print(f"\t{CHANGE_PASS} : CHANGE PASSWORD")   
    print(f"\t{SEE_PROFILE} : SEE PROFILE INFORMATION")
    print(f"\t{EXIT} : Exit")

def handle_services_option(full_name, user_id):
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
            account_service.create_account(full_name, user_id)
        elif option == LOAN:
            clear_console()
            handle_loan_option(account_service.current_account)
        elif option == CHANGE_INFO:
            clear_console()
            User_service.change_info()
        elif option == CHANGE_PASS:
            clear_console()
            User_service.change_pass()
        elif option == SEE_PROFILE:
            clear_console()
            User_service.profile()
        clear_console()
        
def process_fund_transfer(): 
    account_num = input("Enter target account number:")
    amount = float(input("Enter amount to transfer:"))
    transaction_service = TransactionService(account_service.current_account)
    target_account = account_service.find_account_by_number(account_num)
    if target_account != None:
        transaction_service.transfer_fund(target_account, amount)

LOGIN, CREATE = (1, 2)

def login_account_menu(full_name, user_id):
    clear_console()
    #Allow the user to log in or create a new account
    print("Choose an option")
    print(f"\t{LOGIN} : LOGIN ACCOUNT")
    print(f"\t{CREATE} : CREATE ACCOUNT")
    print(f"\t{EXIT} : EXIT")
    choice = int(input("CHOICE: "))

    if choice == LOGIN:
        account_service.select_account()
    elif choice == CREATE:
        account_service.create_account(full_name, user_id)
    else:
        return

def handle_account_option(full_name, user_id):
    #Handle the account options menu and perform related actions
    option = SERVICES
    transaction_service: TransactionService
    login_account_menu(full_name, user_id)
    

    while option != EXIT and account_service.current_account != None:
        clear_console()
        transaction_service = TransactionService(account_service.current_account)
        print_account_menu()
        try:
            option = int(input("\n\tCommand: "))
            clear_console()
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if option == SERVICES:
            clear_console()
            handle_services_option(full_name, user_id)
        elif option == SELECT:
            account_service.select_account()
        #ALI -WITHDRAW    
        elif option == WITHDRAW:
            # variables for arguments in withdrawal function
            account_type = account_service.current_account.account_type
            account_number = account_service.current_account.account_number
            
            with open("data/accounts.json", 'r') as file:
                accounts_data = json.load(file)
                for acc in accounts_data:
                    if acc["account_number"] == account_service.current_account.account_number:
                        balance = acc["balance"] # updated ang balance 
                
            if account_service.current_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            try:
                amount = float(input("\nEnter amount to withdraw: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            
            print(f'__'*20)
            print("\n\tSelected Account")
            print(f"\nSelected account: {full_name} - Account Number: {account_service.current_account.account_number}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
            print(f'__'*20)
            transaction_service.withdrawal(amount, user_id,account_type, account_number, balance)
            input("\nPress any keys to go back to menu")
        #THAMEENAH -DEPOSIT
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu
        elif option == DEPOSIT:
            # variables for arguments in deposit function
            account_type = account_service.current_account.account_type
            account_number = account_service.current_account.account_number
            
            with open("data/accounts.json", 'r') as file:
                accounts_data = json.load(file)
                for acc in accounts_data:
                    if acc["account_number"] == account_service.current_account.account_number:
                        balance = acc["balance"] # updated ang balance 
                
            if account_service.current_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            try:
                amount = float(input("\nEnter amount to deposit: "))
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            
            print(f'__'*20)
            print("\n\tSelected Account")
            print(f"\nSelected account: {full_name} - Account Number: {account_service.current_account.account_number}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
            print(f'__'*20)
            transaction_service.deposit(amount, user_id,account_type, account_number, balance)
            input("\nPress any keys to go back to menu")
            
            
            
        #NORHAILAH   - balance inquiry
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu 
        elif option == BALANCE:
            account_type = account_service.current_account.account_type
            account_number = account_service.current_account.account_number
            
            with open("data/accounts.json", 'r') as file:
                accounts_data = json.load(file)
                for acc in accounts_data:
                    if acc["account_number"] == account_service.current_account.account_number:
                        balance = acc["balance"] # updated ang balance 
           
            if account_service.current_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            
            print(f'__'*20)
            print("\n\tSelected Account")
            print(f"\nSelected account: {full_name} - Account Number: {account_service.current_account.account_number}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
            print(f'__'*20)
            
            transaction_service.balance_inquiry(user_id,account_number)
            
        elif option == TRANSACTION_HISTORY:
            account_type = account_service.current_account.account_type
            account_number = account_service.current_account.account_number
            
            with open("data/accounts.json", 'r') as file:
                accounts_data = json.load(file)
                for acc in accounts_data:
                    if acc["account_number"] == account_service.current_account.account_number:
                        balance = acc["balance"] # updated ang balance 
           
            if account_service.current_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            
            print(f'__'*20)
            print("\n\tSelected Account")
            print(f"\nSelected account: {full_name} - Account Number: {account_service.current_account.account_number}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
            print(f'__'*20)

            transaction_service.display_transactions(user_id,account_type, account_number)
            os.system("pause")
            clear_console()

            clear_console()
            
        elif option == EXIT:
            clear_console()
            return
        elif option == TRANSFER_FUND:
            
            target_account_number = input("Enter the target account number to transfer to: ")
            if target_account_number == account_service.current_account.account_number:
                print("You cannot transfer funds to your own account.")
                input("Press enter to continue")
                return

            try:
                amount = float(input("Enter the amount to transfer: "))
            except ValueError:
                print("Invalid amount entered.")
                input("Press enter to continue")
                return

            if amount <= 0:
                print("Transfer amount must be greater than zero.")
                input("Press enter to continue")
                return

            target_account = None
            for acc in account_service.accounts:
                if acc.account_number == target_account_number:
                    target_account = acc
                    break

            if not target_account:
                print("Target account not found.")
                input("Press enter to continue")
                return

            if account_service.current_account.balance < amount:
                print("Insufficient funds for transfer.")
                input("Press enter to continue")
                return

            
            original_sender_balance = account_service.current_account.balance
            account_service.current_account.balance -= amount
            
            original_receiver_balance = target_account.balance
            target_account.balance += amount

            
            account_service.save_accounts()

            
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_number = str(random.randint(1000000, 9999999))

            debit_transaction = {
                "account_number": account_service.current_account.account_number,
                "user_id": account_service.current_account.user_id,
                "account_type": account_service.current_account.account_type,
                "transaction_type": "debit",
                "date": date,
                "transaction_number": transaction_number,
                "original_balance": original_sender_balance,
                "amount": -amount
            }

            credit_transaction = {
                "account_number": target_account.account_number,
                "user_id": target_account.user_id,
                "account_type": target_account.account_type,
                "transaction_type": "credit",
                "date": date,
                "transaction_number": transaction_number,
                "original_balance": original_receiver_balance,
                "amount": amount
            }

            
            transaction_file = "data/transactions.json"
            try:
                if os.path.exists(transaction_file):
                    with open(transaction_file, 'r') as file:
                        transactions_data = json.load(file)
                else:
                    transactions_data = []
            except (FileNotFoundError, json.JSONDecodeError):
                transactions_data = []

            transactions_data.append(debit_transaction)
            transactions_data.append(credit_transaction)

            with open(transaction_file, 'w') as transaction_file_obj:
                json.dump(transactions_data, transaction_file_obj, indent=4)

            print(f"Transferred ₱{amount:.2f} from {account_service.current_account.account_number} to {target_account.account_number}.")
            input("Press enter to continue")
            
        elif option == GENERATE_REPORT:
            # Generate a report of the account
            print("Generating report...")
            transaction_service.generate_report()
            input("Press enter to continue")

        elif option == FILTER_TRANSACTION_HISTORY:
            filter_transaction_history()

def filter_transaction_history():
    """
    Prompts the user for filter options and displays filtered transaction history.
    """
    transaction_service = TransactionService(account_service.current_account)
    print("\n=== Filter Transaction History ===")
    print("Leave blank if you don't want to filter by that field.")

    transaction_type = input("Transaction Type (deposit/withdrawal/credit/debit): ").strip() or None
    start_date = input("Start Date (YYYY-MM-DD): ").strip() or None
    end_date = input("End Date (YYYY-MM-DD): ").strip() or None
    min_amount = input("Minimum Amount: ").strip()
    max_amount = input("Maximum Amount: ").strip()

    # Convert amount inputs to float if provided
    min_amount = float(min_amount) if min_amount else None
    max_amount = float(max_amount) if max_amount else None

    user_id = account_service.current_account.user_id
    account_number = account_service.current_account.account_number

    transaction_service.filter_transactions(
        user_id=user_id,
        account_number=account_number,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount
    )
    os.system("pause")
    clear_console()