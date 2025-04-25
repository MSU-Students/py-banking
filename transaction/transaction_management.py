import json
from typing import List, Optional
from datetime import datetime
from loan import Loan, LoanPayment
from account import BankAccount

#this holds the container or variables from the data file na need ng class TransactionService para sa isang account
#dito yung mga methods ng pagconvert ng mga needed info into a dictionary format
class Transaction:
    def __init__(self, user_id:str, account_type:str, account_number:int , transaction_number:int, transaction_type: str, date: str, amount: float):
        self.user_id = user_id #lucmanBanking12
        self.account_type = account_type #savings account
        self.account_number = account_number #12345678910
        self.transaction_number = transaction_number
        self.transaction_type = transaction_type  # deposit | withdraw | transfer funds
        self.date = date #2025-04-23 18:19:15
        self.amount = amount #how much amount did you do for diff. transaction

    #function para i store yung new information sa transactions.json, converts yung transaction as dictionary
    def to_dict(self):
        return { 
                "user_id: ":self.user_id,
                "acount_type: ": self.account_type, 
                "account_number": self.account_number,
                "transaction_number: ": self.transaction_number,
                "transaction_type: ": self.transaction_type, 
                "date": self.date, 
                "amount": self.amount  
        }
        
    @staticmethod #static method  - para lang to sa class na transaction, useful to para mag gamit or magcreate ng users' info from transactions.json 
    
    #function para kunin yung information from transactions.json
    def from_dict(data):
        #create/get the user(instance) objects(user_id,account_type...) from key-paired dictionary.
        (
                user_id=data["user_id: "],
                acount_type=data["user_id: "],
                account_number=data["user_id: "],
                transaction_number=data["transaction_number: "],
                transaction_type=data["transaction_type: "],
                date=data["date: "],
                amount=data["amount: "]
        )
#provides the service layer for managing transactions
# nandito yung loading, saving datas, processing em
# offers methods for depositing, withdrawing, transferring, viewing account balance, fund trasferring                           
class TransactionService:
    #store in variable transactions yung lists of user objects from class Transaction
    transactions: List[Transaction] = []

    def __init__(self, account: BankAccount, storage_file: str = "transactions.json"):
        #protected yung account para
        self._account = account
        self.storage_file = storage_file

    def _load_transactions(self):
        try:
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.transactions = [Transaction.from_dict(tx) for tx in data]
        except FileNotFoundError:
            self.transactions = []
        except Exception as e:
            print(f"An error occurred while loading transactions: {e}")

    def _save_transactions(self):
        try:
            with open(self.storage_file, "w") as file:
                json.dump([tx.to_dict() for tx in self.transactions], file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving transactions: {e}")

    def deposit(self, amount: float):
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be greater than zero.")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
            self._account.balance += amount
            transaction = Transaction(account_type="deposit", date=date, amount=amount)
            self.transactions.append(transaction)
            self._save_transactions()
            print(f"Deposited {amount}. New balance: {self._account.balance}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")

    def withdrawal(self, amount: float):
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be greater than zero.")
            if amount > self._account.balance:
                raise ValueError("Insufficient balance.")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
            self._account.balance -= amount
            transaction = Transaction(account_type="withdrawal", date=date, amount=amount)
            self.transactions.append(transaction)
            self._save_transactions()
            print(f"Withdrew {amount}. New balance: {self._account.balance}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An error occurred: {e}")

    def display_transactions(self):
        try:
            if not self.transactions:
                print("No transactions available.")
                return
            print("Transaction History:")
            for transaction in self.transactions:
                print(f"{transaction.date} - {transaction.account_type} - {transaction.amount}")
        except Exception as e:
            print(f"An error occurred while displaying transactions: {e}")

    def filter_transactions(self, date: Optional[str] = None, account_type: Optional[str] = None):
        try:
            filtered = self.transactions
            if date:
                filtered = [tx for tx in filtered if tx.date.startswith(date)]
            if account_type:
                filtered = [tx for tx in filtered if tx.account_type == account_type]
            if not filtered:
                print("No transactions match the filter criteria.")
                return
            print("Filtered Transactions:")
            for transaction in filtered:
                print(f"{transaction.date} - {transaction.account_type} - {transaction.amount}")
        except Exception as e:
            print(f"An error occurred while filtering transactions: {e}")

    def balance_inquiry(self):
        try:
            print(f"Current balance: {self._account.balance}")
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
