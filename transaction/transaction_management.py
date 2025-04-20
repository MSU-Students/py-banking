from typing import List
from loan import Loan, LoanPayment
from account import BankAccount

class Transaction:
    def __init__(self, type: str, date: str, amount: float):
        self.type = type  # deposit | withdraw | transfer
        self.date = date
        self.amount = amount

class TransactionService:
    transactions: List[Transaction] = []

    def __init__(self, account: BankAccount):
        self._account = account

        def deposit(self, amount: float, date: str):
            try:
                if amount <= 0:
                    raise ValueError("Deposit amount must be greater than zero.")
                self._account.balance += amount
                transaction = Transaction(type="deposit", date=date, amount=amount)
                self.transactions.append(transaction)
                print(f"Deposited ₱{amount:.2f} on {date}. New balance: ₱{self._account.balance:.2f}")
            except ValueError as e:
                print(f"Error during deposit: {e}")

    def withdrawal(self, amount: float, date: str):
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if amount > self._account.balance:
                raise ValueError("Insufficient funds.")
            self._account.balance -= amount
            transaction = Transaction(type="withdraw", date=date, amount=amount)
            self.transactions.append(transaction)
            print(f"Withdrew ₱{amount:.2f} on {date}. New balance: ₱{self._account.balance:.2f}")
        except ValueError as e:
            print(f"Error during withdrawal: {e}")

    def display_transactions(self):
        try:
            if not self.transactions:
                print("No transactions available.")
                return
            print("Transaction History:")
            for transaction in self.transactions:
                print(f"{transaction.date} - {transaction.type.capitalize()}: ₱{transaction.amount:.2f}")
        except Exception as e:
            print(f"Error displaying transactions: {e}")


