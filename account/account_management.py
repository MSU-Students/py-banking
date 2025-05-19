from typing import List
from .bank_account import BankAccount
from loan import handle_loan_option
from utils import clear_console
from transaction import TransactionService
import datetime
from random import Random
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

    def create_account(self):
        account : str
        from users.user_management import User_service
        try:
            balance = float(input("Enter initial deposit amount: "))
        except ValueError: 
            print("Invalid input for balance.")
            return
            
        if balance < 500:
            print("Insufficient balance, please deposit at least 500 php.")
            input("press enter to continue...")
            return
            
        SAVINGS, JOINT, STUDENT, BUSINESS, PERSONAL = (1, 2, 3, 4, 5)
        print("choose the type of your account:")
        print(f"\t{SAVINGS} : SAVINGS ACCOUNT")
        print(f"\t{JOINT} : JOINT ACCOUNT")
        print(f"\t{STUDENT} : STUDENT ACCOUNT")
        print(f"\t{BUSINESS} : BUSINESS ACCOUNT")
        print(f"\t{PERSONAL} : PERSONAL ACCOUNT")
        option = int(input("Choice:\t"))

        if option == SAVINGS: account = "Savings Account"
        elif option == JOINT: account = "Joint Account"
        elif option == STUDENT: account = "Student Account"
        elif option == BUSINESS: account = "Business Account"
        elif option == PERSONAL: account = "Personal Account"
        else: return

        new_account = BankAccount(User_service.login_user.User_Id, account, balance, User_service.login_user.name)
        self.accounts.append(new_account)
        self.current_account = new_account
        self.save_accounts()

        print(f"\nAccount created successfully for {new_account.account_type}!")
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
            print(f"{i}. {acc.account_type} - Account ID: {acc.account_id} - Balance: ₱{acc.balance:.2f}")
        return user_accounts


    def select_account(self):
        user_accounts = self.list_accounts()
        if not user_accounts:
            return

        try:
            choice = int(input("\nEnter the number of the account to select: "))
            if 1 <= choice <= len(user_accounts):
                self.current_account = user_accounts[choice - 1]
                print(f"\nSelected account: {self.current_account.account_type} - Balance: ₱{self.current_account.balance:.2f}\n")
            else:
                print("Invalid choice.")
                input("Press enter to continue...")
                return
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

EXIT, WITHDRAW, DEPOSIT, BALANCE, TRANSACTION_HISTORY, SELECT, SERVICES, TRANSFER_FUND, GENERATE_REPORT, FILTER_TRANSACTION_HISTORY = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

def print_account_menu():
    print("Bank Account Options:")
    print(f"\t{WITHDRAW} : Withdraw")
    print(f"\t{DEPOSIT} : Deposit")
    print(f"\t{BALANCE} : Balance Inquiry")
    print(f"\t{TRANSACTION_HISTORY} : Transaction History")
    print(f"\t{SELECT} : Select Another Account")
    print(f"\t{SERVICES} : Access Services")
    print(f"\t{TRANSFER_FUND} : Fund Transfer")
    print(f"\t{GENERATE_REPORT} : Generate Report")
    print(f"\t{FILTER_TRANSACTION_HISTORY} : Filter Transaction History")
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
def login_account_menu():
    #Allow the user to log in or create a new account
    print("Choose an option")
    print(f"\t{LOGIN} : SELECT ACCOUNT")
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
            print('hello world')

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
            print(f"\nSelected account:\t{account_service.current_account.full_name}\nAccount Number:\t\t{account_service.current_account.account_id}\nAccount Type:\t\t{account_service.current_account.account_type}\nAccount Balance:\t₱{balance:.2f}\n")
            print(f'__'*20)
            transaction_service.withdrawal(amount, user_id,account_type, account_number, balance)
            input("\nPress any keys to go back to menu")

            transaction_service.withdrawal(amount, account_service.current_account.user_id,account_type, account_id, balance)
            input("\nPress any keys to go back to menu")
        #THAMEENAH -DEPOSIT
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu
        elif option == DEPOSIT:
            # variables for arguments in deposit function
            account_type = account_service.current_account.account_type
            account_id = account_service.current_account.account_id
            
            with open("data/accounts.json", 'r') as file:
                accounts_data = json.load(file)
                for acc in accounts_data:
                    if acc["account_id"] == account_service.current_account.account_id:
                        balance = acc["balance"] # updated ang balance 
                
            if account_service.current_account is None:
                continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select

            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    return
            except ValueError:
                print("Invalid amount. Please enter a number.")
                continue
            
            print(f'__'*20)
            print("\n\tSelected Account")
            print(f"\nSelected account:\t{account_service.current_account.full_name}\nAccount Number:\t\t{account_service.current_account.account_id}\nAccount Type:\t\t{account_service.current_account.account_type}\nAccount Balance:\t₱{balance:.2f}\n")
            print(f'__'*20)
            transaction_service.deposit(amount, account_service.current_account.user_id,account_type, account_id, balance)
            input("\nPress any keys to go back to menu")

            
            
        #NORHAILAH   - balance inquiry
        #CHRISTIAN - EXCEPTION HANDLING - pagandahin mo yung mga ganern lods, may retries chuchu, while loops chuchu 
        elif option == BALANCE:
             def balance_inquiry(self, user_id: str, account_number: str):
                try:
                    with open("accounts.json", 'r') as file:
                        accounts = json.load(file)
                        for account in accounts:
                            if account.get("account_number") == account_number and account.get("user_id") == user_id:
                                print(f"User ID: {user_id}")
                                print(f"Account Type: {account.get('account_type')}")
                                print(f"Account Number: {account_number}")
                                print(f"Current Balance: ₱{account.get('account_balance'):,.2f}")
                                return
                        print("Account not found.")
                except FileNotFoundError:
                    print("Accounts file not found.")
                except json.JSONDecodeError:
                    print("Error decoding the accounts file.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    
                    clear_console()

        #     account_type = account_service.current_account.account_type
        #     account_id = account_service.current_account.account_id
            
        #     with open("data/accounts.json", 'r') as file:
        #         accounts_data = json.load(file)
        #         for acc in accounts_data:
        #             if acc["account_id"] == account_service.current_account.account_id:
        #                 balance = acc["balance"] # updated ang balance 
           
        #     if account_service.current_account is None:
        #         continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            
        #     print(f'__'*20)
        #     print("\n\tSelected Account")
        #     print(f"\nSelected account: {account_service.current_account.full_name} - Account Number: {account_service.current_account.account_id}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
        #     print(f'__'*20)
            
        #     transaction_service.balance_inquiry(account_service.current_account.user_id,account_id)
            
        # elif option == TRANSACTION_HISTORY:
        #     account_type = account_service.current_account.account_type
        #     account_id = account_service.current_account.account_id
            
        #     with open("data/accounts.json", 'r') as file:
        #         accounts_data = json.load(file)
        #         for acc in accounts_data:
        #             if acc["account_id"] == account_service.current_account.account_id:
        #                 balance = acc["balance"] # updated ang balance 
           
        #     if account_service.current_account is None:
        #         continue # skips the iteration , no account is selected(or the user did not choose a valid acc) kaya i ask niya uli ang user anong account i select
            
        #     print(f'__'*20)
        #     print("\n\tSelected Account")
        #     print(f"\nSelected account: {account_service.current_account.full_name} - Account Number: {account_service.current_account.account_id}\n{account_service.current_account.account_type} Account - Balance: ₱{balance:.2f}\n")
        #     print(f'__'*20)
        #     transaction_service.display_transactions(account_service.current_account.user_id,account_type, account_id)
        #     os.system("pause")
        #     clear_console()
        # elif option == EXIT:
            # clear_console()
            # return
           
          
          transaction_service.display_transactions(account_service.current_account.user_id,account_type, account_id)
            os.system("pause")
            clear_console()

            clear_console()
            
        elif option == EXIT:
            clear_console()
            return
        elif option == TRANSFER_FUND:
            
            target_account_id = int(input("Enter the target account number to transfer to: "))
            if target_account_id == account_service.current_account.account_id:
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
                if acc.account_id == target_account_id:
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
                "account_id": account_service.current_account.account_id,
                "user_id": account_service.current_account.user_id,
                "account_type": account_service.current_account.account_type,
                "transaction_type": "debit",
                "date": date,
                "transaction_number": transaction_number,
                "original_balance": original_sender_balance,
                "amount": -amount
            }

            credit_transaction = {
                "account_id": target_account.account_id,
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

            print(f"Transferred ₱{amount:.2f} from {account_service.current_account.account_id} to {target_account.account_id}.")
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
    account_id = account_service.current_account.account_id

    transaction_service.filter_transactions(
        user_id=user_id,
        account_id=account_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount
    )
    os.system("pause")
    clear_console()
