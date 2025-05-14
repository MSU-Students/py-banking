from typing import List
from utils import clear_console
from account import BankAccount

class Loan:
    user_id: int
    id: int
    status: str # pending, approve, paid, paying
    balance: float

class LoanPayment:
    loan_id: int
    amount: float
    date: str

class LoanService:
    current_loan: Loan | None = None
    loans: List[Loan] = []
    payments: List[LoanPayment] = []

    def __init__(self, account: BankAccount):
        self._bank_account = account

    def loan_apply(self):
        amount = float(input("Enter loan amount: "))
        loan_id = len(self.loans) + 1  
        new_loan = Loan(self._bank_account.user_id, loan_id, amount)
        self.loans.append(new_loan)
        print(f"Loan application submitted: ID {loan_id}, Amount {amount}")

    def collect_payment(self):
        loan_id = int(input("Enter loan ID to make a payment: "))
        amount = float(input("Enter payment amount: "))
        date = input("Enter payment date (YYYY-MM-DD): ")

        for loan in self.loans:
            if loan.id == loan_id:
                if loan.status == 'approved' and loan.balance > 0:
                    loan.balance -= amount
                    self.payments.append(LoanPayment(loan_id, amount, date))
                    print(f"Payment of {amount} made for Loan ID {loan_id}. Remaining balance: {loan.balance}")
                    if loan.balance <= 0:
                        loan.status = 'paid'
                        print(f"Loan ID {loan_id} is now fully paid.")
                else:
                    print(f"Loan ID {loan_id} is not approved or already paid.")
                return
        print(f"Loan ID {loan_id} not found.")

    def loan_history(self):
        if not self.loans:
            print("No loans found.")
            return

        for loan in self.loans:
            print(f"Loan ID: {loan.id}, Status: {loan.status}, Balance: {loan.balance}")
            loan_payments = [payment for payment in self.payments if payment.loan_id == loan.id]
            for payment in loan_payments:
                print(f"  Payment: {payment.amount} on {payment.date}")

EXIT, LOAN_APPLY, LOAN_PAYMENT, LOAN_HISTORY = 0, 1, 2, 3
def print_loan_option():
    print("Loan Options:")
    print(f"\t{LOAN_APPLY} : Loan Application")
    print(f"\t{LOAN_PAYMENT} : Loan Payment")
    print(f"\t{LOAN_HISTORY} : Loan History")
    #other option here
    print(f"\t{EXIT} : Exit")
    
def handle_loan_option(account: BankAccount):
    loan_service = LoanService(account)
    option = LOAN_PAYMENT
    while option != EXIT:
        print_loan_option()
        option = int(input("\n\tCommand: "))
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
        clear_console()