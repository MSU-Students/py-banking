import json
from typing import List, Optional
from datetime import datetime
# Removed unused imports Loan and LoanPayment
from account import BankAccount
import random


class Transaction:
    def __init__(self, type: str, date: str, amount: float, transaction_number: str, account_number: str = None, account_type: str = None, account_balance: float = None):      
        self.account_number = account_number
        self.account_type = account_type
        self.account_balance = account_balance
        self.transaction_type = type  # deposit | withdraw | transfer
        self.date = date
        self.amount = amount
        self.transaction_number = transaction_number




class TransactionService:
    def __init__(self, account):
        if isinstance(account, dict):
            # Convert dictionary to BankAccount
            account = BankAccount(
                user_id=account["user_id"],
                account_number=account["account_number"],
                account_type=account["account_type"],
                account_balance=account["balance"]
            )
        elif not isinstance(account, BankAccount):
            raise TypeError(f"Expected BankAccount, got {type(account).__name__}")
        self.account = account
        self.transactions: List[Transaction] = []
        self.account_balance = account.account_balance

    def deposit(self, amount: float):
        if amount <= 0.0:
            raise ValueError("Deposit amount must be greater than zero.")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        self.account.account_balance += amount  # Update the account's balance
        transaction_number = str(random.randint(1000000, 9999999))
        transaction = Transaction(type="deposit", date=date, amount=amount, transaction_number=transaction_number)

        self.transactions.append(transaction)
        transaction_data = {
            "user_id": self.account.user_id,
            "account_type": self.account.account_type,
            "account_number": self.account.account_number,
            "transaction_type": transaction.transaction_type,
            "date": transaction.date,
            "transaction_number": transaction.transaction_number,
            "amount": transaction.amount,
        }

        with open("transactions.json", 'a') as file:
            file.write(json.dumps(transaction_data, indent=4) + "\n")
        print(f"Deposited {amount}. New balance: {self.account.account_balance}")
    def withdrawal(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.account.account_balance:
            raise ValueError("Insufficient balance.")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Include time
        self.account.account_balance -= amount
        transaction_number = str(random.randint(1000000, 9999999))
        transaction = Transaction(type="withdrawal", date=date, amount=amount, transaction_number=transaction_number)

        self.transactions.append(transaction)
        transaction_data = {
            "user_id": self.account.user_id,
            "account_type": self.account.account_type,"account_number": self.account.account_number,
            "transaction_type": transaction.transaction_type,  "transaction_number": transaction.transaction_number,
            "amount": transaction.amount, "date": transaction.date
            
        }

        with open("transactions.json", 'a') as file:
            file.write(json.dumps(transaction_data, indent=4) + "\n")
        print(f"Withdrew {amount}. New balance: {self.account.account_balance}")

    def display_transactions(self):
        if not self.transactions:
            print("No transactions available.")
            return
        print("Transaction History:")
        for transaction in self.transactions:
            print(f"{transaction.date} - {transaction.transaction_type} - {transaction.amount}")

    def filter_transactions(self, date: Optional[str] = None, type: Optional[str] = None):
        filtered = self.transactions
        if date:
            filtered = [tx for tx in filtered if tx.date.startswith(date)]
        if type:
            filtered = [tx for tx in filtered if tx.transaction_type == type]
        if not filtered:
            print("No transactions match the filter criteria.")
            return
        print("Filtered Transactions:")
        for transaction in filtered:
            print(f"{transaction.date} - {transaction.transaction_type} - {transaction.amount}")

    def balance_inquiry(self):
        try:
            print(f"Current balance: {self.account.account_balance}")
        except Exception as e:
            print(f"An error occurred while checking balance: {e}")
