import json
from typing import List
from datetime import datetime
from utils import clear_console
from account import BankAccount
from transaction_service import TransactionService

class Loan:
    def __init__(self, user_id: int, loan_id: int, amount: float):
        self.user_id = user_id
        self.id = loan_id
        self.status = 'approved'
        self.balance = amount

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "id": self.id,
            "status": self.status,
            "balance": self.balance
        }

class LoanPayment:
    def __init__(self, loan_id: int, amount: float, date: str):
        self.loan_id = loan_id
        self.amount = amount
        self.date = date

class LoanService:
    loan_file = "data/loan.json"
    payment_file = "data/payments.json"

    def __init__(self, account: BankAccount):
        self._bank_account = account
        self.loans: List[Loan] = []
        self.payments: List[LoanPayment] = []
        self.load_loans()
        self.load_payments()

    def load_loans(self):
        try:
            with open(self.loan_file, 'r') as file:
                loan_data = json.load(file)
                for data in loan_data:
                    self.loans.append(Loan(
                        user_id=data['user_id'],
                        loan_id=data['id'],
                        amount=data['balance']
                    ))
        except (FileNotFoundError, json.JSONDecodeError):
            self.loans = []

    def save_loans(self):
        with open(self.loan_file, 'w') as file:
            json.dump([loan.to_dict() for loan in self.loans], file, indent=4)

    def load_payments(self):
        try:
            with open(self.payment_file, 'r') as file:
                payment_data = json.load(file)
                for data in payment_data:
                    self.payments.append(LoanPayment(
                        loan_id=data['loan_id'],
                        amount=data['amount'],
                        date=data['date']
                    ))
        except (FileNotFoundError, json.JSONDecodeError):
            self.payments = []

    def save_payments(self):
        with open(self.payment_file, 'w') as file:
            json.dump([vars(p) for p in self.payments], file, indent=4)

    def loan_apply(self):
        try:
            amount = float(input("Enter loan amount: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        loan_id = len(self.loans) + 1
        new_loan = Loan(self._bank_account.user_id, loan_id, amount)
        self.loans.append(new_loan)
        self.save_loans()
        print(f"Loan application submitted and automatically approved: ID {loan_id}, Amount {amount}")

    def collect_payment(self):
        try:
            loan_id = int(input("Enter loan ID to make a payment: "))
            amount = float(input("Enter payment amount: "))
        except ValueError:
            print("Invalid input. Please enter numbers for ID and amount.")
            return

        for loan in self.loans:
            if loan.id == loan_id:
                if loan.user_id != self._bank_account.user_id:
                    print("You are not authorized to make payments on this loan.")
                    return
                if loan.status == 'approved' and loan.balance > 0:
                    if amount > loan.balance:
                        print(f"Payment exceeds remaining balance of {loan.balance}")
                        return

                    transaction_service = TransactionService(self._bank_account)
                    success = transaction_service.withdrawal(
                        amount=amount,
                        user_id=self._bank_account.user_id,
                        account_type=self._bank_account.account_type,
                        account_id=self._bank_account.account_id,
                        original_balance=self._bank_account.balance
                    )
                    if success is None:
                        return

                    loan.balance -= amount
                    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    payment = LoanPayment(loan_id, amount, current_date)
                    self.payments.append(payment)
                    print(f"Payment of {amount} made for Loan ID {loan_id}. Remaining balance: {loan.balance}")
                    if loan.balance <= 0:
                        loan.status = 'paid'
                        print(f"Loan ID {loan_id} is now fully paid.")
                    self.save_loans()
                    self.save_payments()
                else:
                    print(f"Loan ID {loan_id} is not approved or already paid.")
                return
        print(f"Loan ID {loan_id} not found.")

    def loan_history(self):
        found = False
        for loan in self.loans:
            if loan.user_id == self._bank_account.user_id:
                found = True
                print(f"\nLoan ID: {loan.id}, Status: {loan.status}, Balance: {loan.balance}")
                loan_payments = [p for p in self.payments if p.loan_id == loan.id]
                for payment in loan_payments:
                    print(f"  Payment: {payment.amount} on {payment.date}")
        if not found:
            print("No loans found for this user.")


EXIT, LOAN_APPLY, LOAN_PAYMENT, LOAN_HISTORY = 0, 1, 2, 3

def print_loan_option():
    print("Loan Options:")
    print(f"\t{LOAN_APPLY} : Loan Application")
    print(f"\t{LOAN_PAYMENT} : Loan Payment")
    print(f"\t{LOAN_HISTORY} : Loan History")
    print(f"\t{EXIT} : Exit")

def handle_loan_option(account: BankAccount):
    loan_service = LoanService(account)
    option = LOAN_PAYMENT
    while option != EXIT:
        print_loan_option()
        try:
            option = int(input("\n\tCommand: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if option == EXIT:
            return
        elif option == LOAN_APPLY:
            loan_service.loan_apply()
        elif option == LOAN_PAYMENT:
            loan_service.collect_payment()
        elif option == LOAN_HISTORY:
            loan_service.loan_history()
        else:
            print("Invalid option. Please try again.")

        input("\nPress Enter to continue...")
        clear_console()
