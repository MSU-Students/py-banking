from typing import List
from loan import Loan, LoanPayment
from account import BankAccount

class Transaction:
    type: str # deposit| withdraw| transfer
    date: str
    amount: float

class TransactionService:
    transactions: List[Transaction] = []

    def __init__(self, account: BankAccount):
        self._account = account
    
    def deposit(self):
        input("TODO: deposit action")

    def withdrawal(self):
        input("TODO: withdrawal action")
    

    def display_transactions(self):
        input("TODO: Transaction list")

