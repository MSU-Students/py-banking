import json
from typing import List, Optional
from datetime import datetime
# Removed unused imports Loan and LoanPayment
# from account import BankAccount
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
    accounts_file = "accounts.json"
    transactions_data = list()
    transaction_file = "transactions.json"
    

    def __init__(self, account: Transaction):
        try:
            if os.path.exists(self.transaction_file):
                with open(self.transaction_file, 'r') as file:
                    self.transactions_data = json.load(file)
        #if walang laman talaga and transactions.json, as in walang brackets, mag lalagay siya ng empty bracket doon 
        except(FileNotFoundError, json.JSONDecodeError):
            self.transactions_data = []
        self.account = account
        print(f'__'*20)
        print("\n\tTRANSACTION SERVICE")
        print(f'__'*20)

#NORHAILAH - DEPOSIT
    def deposit(self, amount: float, user_id:str, account_type:str, account_number:str, account_balance:float):
        if amount <= 0.0:
            raise ValueError("Deposit amount must be greater than zero.")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        
        account_balance += amount  # Update the account's balance
        transaction_number = str(random.randint(1000000, 9999999))
        self.account = Transaction(user_id=user_id,account_type=account_type,account_number=account_number,type="deposit", date=date, amount=amount, transaction_number=transaction_number,original_balance=account_balance)
        #para to sa original balance bago pa nag deposit si user
        self.account.original_balance -= amount
        
                    
        #turn it into a dictionary
        datas = {
            "account_number: ": self.account.account_number,
            "user_id: ": self.account.user_id,
            "account_type: ": self.account.account_type,
            "transaction_type: ": self.account.transaction_type,
            "date: ": self.account.date,
            "transaction_number: ": self.account.transaction_number,
            "original_balance: ": self.account.original_balance,
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

            
        print(f"Deposited: {amount}. New balance: {account_balance}")

        #im not sure if gagana na hindi ma overwrite and accounts.json para lang ma update yung account_balance ng isang account sa accounts.json
        with open("accounts.json", 'r') as file:
            accounts = json.load(file)
            for i, account in enumerate(accounts):
                if account["account_number: "] == account_number:
                    accounts[i]["account_balance: "] = account_balance
                    with open("accounts.json", 'w') as file:  
                       pass
                    break
        with open("accounts.json", 'a') as file:  
            json.dump(accounts, file, indent=4)

        print(f'\n\tSucessful Transaction!\nAccount Type: {self.account.account_type}\t Account Number: {self.account.account_number}\t Transaction Number: {self.account.transaction_number}')

    #ALI - WITHDRAWAL
    # CHRISTIAN - INSUFFIECIENT CHUCHU, iKAW BAHALA GUMAWA NG WHILE LOOPS AND EXCEPTION HANDLING
    def withdrawal(self, amount: float, user_id:str, account_type:str, account_number:str, account_balance:float):
        while True:
            if amount <= 0:
                print("Withdraw amount must be greater than zero.")
                return

            if amount > account_balance:
                print("Insufficient funds for withdrawal.")
                return

            if account_balance - amount < 500:
                print("Wirhdrawal amount must not exceed the amount balance minus the maintaining balance of Php 500.")
                return
                
            if account_balance - amount >= 500:       
    
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
                
                account_balance -= amount  # Update the account's balance
                transaction_number = str(random.randint(1000000, 9999999))
                self.account = Transaction(user_id=user_id,account_type=account_type,account_number=account_number,type="withdrawal", date=date, amount=amount, transaction_number=transaction_number,original_balance=account_balance)
                #para to sa original balance bago pa nag withdraw si user
                self.account.original_balance += amount
                
                datas = {
                    "account_number: ": self.account.account_number,
                    "user_id: ": self.account.user_id,
                    "account_type: ": self.account.account_type,
                    "transaction_type: ": self.account.transaction_type,
                    "date: ": self.account.date,
                    "transaction_number: ": self.account.transaction_number,
                    "original_balance: ": self.account.original_balance,
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
            
            
                print(f"Deposited: {amount}. New balance: {account_balance}")
                
            #update the account balance of the selected user's account in accounts.json
                with open("accounts.json", 'r') as file:
                    accounts = json.load(file)
                    for i, account in enumerate(accounts):
                        if account["account_number: "] == account_number:
                            accounts[i]["account_balance: "] = account_balance
                            with open("accounts.json", 'w') as file:  
                                pass
                            break
                with open("accounts.json", 'a') as file:  
                    json.dump(accounts, file, indent=4)

                print(f'\n\tSucessful Transaction!\nAccount Type: {self.account.account_type}\t Account Number: {self.account.account_number}\t Transaction Number: {self.account.transaction_number}')
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
            with open("transactions.json", 'r') as file:
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
             with open("accounts.json", 'r') as file:
                accounts = json.load(file)
                for i, account in enumerate(accounts):
                    if account["account_number: "] == account_number:
                        print(f"User Id: {user_id}")
                        print(f"Account_type:  {account["account_type: "]}")
                        print(f"Account Number: {account_number}")
                        print(f"Current balance: Php {account["account_balance: "]}")
                        return        
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
        except FileNotFoundError as e:
            print("The account.json file does not exist. Please ensure the file as available.")
