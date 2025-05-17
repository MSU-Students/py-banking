import json
from typing import List, Optional
from datetime import datetime
# Removed unused imports Loan and LoanPayment
from account import BankAccount
import random
import os
# from utils import clear_console 

class Transaction:
    def __init__(self, user_id: str, account_type: str,account_number: str, type: str, date: str, amount: float, transaction_number: str, original_balance:float):      
        self.user_id = user_id
        self.account_type = account_type
        self.account_number = account_number
        self.transaction_type = type  # deposit | withdraw | transfer
        self.date = date
        self.amount = amount
        self.transaction_number = transaction_number
        self.original_balance = original_balance



class TransactionService:
    accounts_file = "data/accounts.json"
    transactions_data = list()
    transaction_file = "data/transactions.json"
    

    def __init__(self, account: Transaction):
        try:
            if os.path.exists(self.transaction_file):
                with open(self.transaction_file, 'r') as file:
                    self.transactions_data = json.load(file)
            else:
                with open(self.transaction_file, 'w') as file:
                    file.write('[]')
        #if walang laman talaga and transactions.json, as in walang brackets, mag lalagay siya ng empty bracket doon 
        except(FileNotFoundError, json.JSONDecodeError):
            self.transactions_data = []
        self.account = account
        print(f'__'*20)
        print("\n\tTRANSACTION SERVICE")

#NORHAILAH - DEPOSIT
    def deposit(self, amount: float, user_id:str, account_type:str, account_number:str, original_balance:float):
        if amount <= 0.0:
            raise ValueError("Deposit amount must be greater than zero.")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        
        updated_balance = original_balance
        updated_balance += amount  # Update the account's balance
        
        transaction_number = str(random.randint(1000000, 9999999))
        self.account = Transaction(user_id=user_id,account_type=account_type,account_number=account_number,type="withdrawal", date=date, amount=amount, transaction_number=transaction_number,original_balance=original_balance)
        
                    
        #turn it into a dictionary
        datas = {
            "account_number: ": self.account.account_number,
            "user_id: ": self.account.user_id,
            "account_type: ": self.account.account_type,
            "transaction_type: ": self.account.transaction_type,
            "date: ": self.account.date,
            "transaction_number: ": self.account.transaction_number,
            "original_balance: ": original_balance,
            "amount: ": self.account.amount
        }  
        #if meron siyang brackets, i load niya      
        try:
            if os.path.exists(self.transaction_file):
                with open(self.transaction_file, 'r') as file:
                    self.transactions_data = json.load(file)
        #if walang laman talaga and transactions.json, as in walang brackets, mag lalagay siya ng empty bracket doon 
        except(FileNotFoundError, json.JSONDecodeError):
                self.transactions_data = []
        self.transactions_data.append(datas)
        
        #i store niya na append sa self.transactions_Data doon sa path na self.transactions.file
        with open(self.transaction_file, 'w+') as transaction_file:
            json.dump(self.transactions_data, transaction_file, indent=4)

            
        print(f"Deposited: {amount}. New balance: {updated_balance}")

         #update the account balance of the selected user's account in accounts.json
        with open("data/accounts.json", 'r') as file:
            accounts = json.load(file)
            for i, account in enumerate(accounts):
                if account["account_number"] == account_number:
                    accounts[i]["balance"] = updated_balance
                    with open("data/accounts.json", 'w') as file:  
                       pass
                    break
        with open("data/accounts.json", 'a') as file:  
            json.dump(accounts, file, indent=4)

        print(f'\n\tSucessful Transaction!\nAccount Type: {self.account.account_type}\t Account Number: {self.account.account_number}\t Transaction Number: {self.account.transaction_number}\n')
        print("__"*20)

    #ALI - WITHDRAWAL
    # CHRISTIAN - INSUFFIECIENT CHUCHU, iKAW BAHALA GUMAWA NG WHILE LOOPS AND EXCEPTION HANDLING
    def withdrawal(self, amount: float, user_id:str, account_type:str, account_number:str, original_balance:float):
        while True:
            if amount <= 0:
                print("Withdraw amount must be greater than zero.")
                return

            if amount > original_balance:
                print("Insufficient funds for withdrawal.")
                return

            if original_balance - amount < 500:
                print("Wirhdrawal amount must not exceed the amount balance minus the maintaining balance of Php 500.")
                return
                
            if original_balance - amount >= 500:       
    
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
                
                updated_balance = original_balance
                updated_balance -= amount  # Update the account's balance
                
                #transaction number
                transaction_number = str(random.randint(1000000, 9999999))
                self.account = Transaction(user_id=user_id,account_type=account_type,account_number=account_number,type="withdrawal", date=date, amount=amount, transaction_number=transaction_number,original_balance=original_balance)
                
                #para to sa original balance bago pa nag withdraw si user

                
                
                datas = {
                    "account_number: ": self.account.account_number,
                    "user_id: ": self.account.user_id,
                    "account_type: ": self.account.account_type,
                    "transaction_type: ": self.account.transaction_type,
                    "date: ": self.account.date,
                    "transaction_number: ": self.account.transaction_number,
                    "original_balance: ": original_balance,
                    "amount: ": self.account.amount
                }
                
                #if meron siyang brackets, i load niya      
                try:
                    if os.path.exists(self.transaction_file):
                        with open(self.transaction_file, 'r') as file:
                            self.transactions_data = json.load(file)
                #if walang laman talaga and transactions.json, as in walang brackets, mag lalagay siya ng empty bracket doon 
                except(FileNotFoundError, json.JSONDecodeError):
                        self.transactions_data = []
                self.transactions_data.append(datas)
                
                #i store niya na append sa self.transactions_Data doon sa path na self.transactions.file
                with open(self.transaction_file, 'w+') as transaction_file:
                    json.dump(self.transactions_data, transaction_file, indent=4)
            
            
                print(f"Deposited: {amount}. New balance: {updated_balance}")
                
            #update the account balance of the selected user's account in accounts.json
                with open("data/accounts.json", 'r') as file:
                    accounts = json.load(file)
                    for i, account in enumerate(accounts):
                        if account["account_number"] == account_number:
                            accounts[i]["balance"] = updated_balance
                            with open("data/accounts.json", 'w') as file:  
                                pass
                            break
                with open("data/accounts.json", 'a') as file:  
                    json.dump(accounts, file, indent=4)

                print(f'\n\tSucessful Transaction!\n\nAccount Type: {self.account.account_type}\t Account Number: {self.account.account_number}\t Transaction Number: {self.account.transaction_number}\n')
                print("__"*20)
                return
            else:
                print("Invalid Input. Please try again.")
                return
            
            
    # group 2 -christian (handling insuffiecient errors ) - ikaw na bahala mag gawa ng while loop dito
    # IKAW na bahala sano history transaction kapag ang account number walang laman na transaction history, gawan mo ng exception handling, and yung mga error messages
    def display_transactions(self, user_id:str, account_type:str, account_number:str):
        print(f"User Id: {user_id}") 
        print(f"Account Type: {account_type}") 
        print(f"Account Number:{account_number}")
        print(f"\n\t\tList of Transactions\n")   

        try:
            with open("data/transactions.json", 'r') as file:
                transactions = json.load(file)
                i = 0
                for transaction in transactions:

                    if transaction["user_id: "] == user_id and transaction["account_number: "] == account_number:
                        print(f"{i+1.}\n* Date and Time: {transaction["date: "]} \n* Transaction Type: {transaction["transaction_type: "]} \n* Amount: {transaction["amount: "]}\n* Transaction Number: {transaction["transaction_number: "]}")
                        i+=1
                if i == 0:
                    raise ValueError("No transactions found for this account.")
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def balance_inquiry(self, user_id:str,account_number:str):
        try:
             with open("data/accounts.json", 'r') as file:
                accounts = json.load(file)
                for i, account in enumerate(accounts):
                    if account["account_number"] == account_number:
                        print("\tBALANCE INQUIRY\n")
                        print(f"User Id: {user_id}")
                        print(f"Account_type:  {account["account_type"]}")
                        print(f"Account Number: {account_number}")
                        print(f"Current balance: Php {account["balance"]}\n")
                        print("__"*20)
                        input("Press any key to go back to menu")
                        return        
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
        except FileNotFoundError as e:
            print("The account.json file does not exist. Please ensure the file as available.")

            

    def transfer_fund(self, target_account: BankAccount, amount: float):
            if amount <= 0:
                print("Transfer amount must be greater than zero.")
                return

            if self._account.balance < amount:
                print("Insufficient funds for transfer.")
                return

            self._account.balance -= amount
            print(f"Transferred {amount} from {self._account.account_number}.")
            transaction = Transaction(type="credit", date="", amount=amount, account_num=self._account.account_number)
            self.transactions.append(transaction)
            self._save_transactions()


            target_account.balance += amount
            print(f"Received {amount} in {target_account.account_number}.")
            transaction = Transaction(type="debit", date="", amount=amount, account_num=target_account.account_number)
            self.transactions.append(transaction)
            self._save_transactions()
            input("Press enter to continue")

    def generate_report(self):
        try:
            report = {
                "Account Report": {
                    "User ID": self._account.user_id,
                    "Account Name": self._account.account_name,
                    "Account Number": self._account.account_number,
                    "Current Balance": self._account.balance,
                },
                "Transaction Summary": {
                    "Total Deposits": sum(tx.amount for tx in self.transactions if tx.type == "deposit"),
                    "Total Withdrawals": sum(tx.amount for tx in self.transactions if tx.type == "withdrawal"),
                    "Total Transactions": len(self.transactions),
                },
                "Transactions": [tx.to_dict() for tx in self.transactions],
                "Report Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            with open("data/Generate_Report.json", "w") as file:
                json.dump(report, file, indent=4)
            print("Report generated successfully.")
        except Exception as e:
            print(f"An error occurred while generating the report: {e}")
