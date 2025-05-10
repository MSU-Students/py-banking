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
    loans : List[Loan] = []
    payments: List[LoanPayment] = []
    
    def __init__(self, account: BankAccount):
        self._bank_account = account

    def loan_apply(self):
        print("TODO:loan application")
        input("press any key")
    
    def collect_payment(self):
        print("TODO: Collect Payment")
    
    def display_load_history(self):
        print("TODO: Loan History")
    # Other methods here like (history, ....)



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
        # handle other options here
        clear_console()