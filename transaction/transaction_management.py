import json
from typing import List, Optional
from datetime import datetime
from loan import Loan, LoanPayment
from account import BankAccount

class Transaction:
    def __init__(self, type: str, date: str, amount: float):
        self.type = type  # deposit | withdraw | transfer
        self.date = date
        self.amount = amount

    def to_dict(self):
        return {"type": self.type, "date": self.date, "amount": self.amount}

    @staticmethod
    def from_dict(data):
        return Transaction(type=data["type"], date=data["date"], amount=data["amount"])

class TransactionService:
    transactions: List[Transaction] = []

    def __init__(self, account: BankAccount, storage_file: str = "transactions.json"):
        self._account = account
        self.storage_file = storage_file
        self._load_transactions()

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
            transaction = Transaction(type="deposit", date=date, amount=amount)
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
            transaction = Transaction(type="withdrawal", date=date, amount=amount)
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
                print(f"{transaction.date} - {transaction.type} - {transaction.amount}")
        except Exception as e:
            print(f"An error occurred while displaying transactions: {e}")

    def filter_transactions(self, date: Optional[str] = None, type: Optional[str] = None):
        try:
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
        except Exception as e:
            print(f"An error occurred while filtering transactions: {e}")

    def balance_inquiry(self):
        try:
            print(f"Current balance: {self._account.balance}")
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
