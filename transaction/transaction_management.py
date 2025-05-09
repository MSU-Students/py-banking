import json
from typing import List, Optional
from datetime import datetime
from loan import Loan, LoanPayment
from account import BankAccount
import random

class Transaction:
    def __init__(self, type: str, date: str, amount: float, transaction_number:str):
        self.transaction_type = type  # deposit | withdraw | transfer
        self.date = date
        self.amount = amount
        self.transaction_number = transaction_number
      
        

user_Details:BankAccount
class TransactionService:
    transactions: List[Transaction] = []

    def __init__(self, account: BankAccount):
        self.account = account



    def deposit(self, amount:float):

        if amount <= 0.0:
            raise ValueError("Deposit amount must be greater than zero.")
        
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        self.account.account_balance += amount
        self.amount = amount
        self.transaction_number = str(random.randint(1000000, 9999999))
        self.transaction_type = "deposit"
        self.user_id = user_Details.user_id
        self.account_type = user_Details.account_type
        self.account_number = user_Details.account_balance
    
        transaction_data={
            "user_id: ": self.user_id,
            "account_type: ": self.account_type, "account_number: ": self.account_number,
            "transaction_type: ":self.transaction_type, "date: ":self.date,
            "transaction_number": self.transaction_number, "amount_deposited: ":self.amount
        }
        
        self.transactions.append(transaction_data)
        #append
        with open ("transactions.json", 'a') as file:
            file.write(transaction_data)
        print(f"Deposited {amount}. New balance: {self.account.account_balance}")
    

    def withdrawal(self, amount: float):
     
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.account.balance:
            raise ValueError("Insufficient balance.")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        self.account.balance -= amount
        transaction = Transaction(type="withdrawal", date=date, amount=amount)
        
        self.transactions.append(transaction)
        self._save_transactions()
        print(f"Withdrew {amount}. New balance: {self.account.balance}")


    def display_transactions(self):
    
        if not self.transactions:
            print("No transactions available.")
            return
        print("Transaction History:")
        for transaction in self.transactions:
            print(f"{transaction.date} - {transaction.type} - {transaction.amount}")


    def filter_transactions(self, date: Optional[str] = None, type: Optional[str] = None):
       
        filtered = self.transactions
        if date:
            filtered = [tx for tx in filtered if tx.date.startswith(date)]
        if type:
            filtered = [tx for tx in filtered if tx.type == type]
        if not filtered:
            print("No transactions match the filter criteria.")
            return
        print("Filtered Transactions:")
        for transaction in filtered:
            print(f"{transaction.date} - {transaction.type} - {transaction.amount}")

    def balance_inquiry(self):
        try:
            print(f"Current balance: {self.account.balance}")
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
