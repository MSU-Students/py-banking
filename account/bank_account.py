
class BankAccount:
    user_id: int
    account_type: str
    account_number: str
    account_balance: float


    def __init__(self, user_id:int, account_type:str, account_number: str, account_balance: float = 0.0):
        self.user_id = user_id
        self.account_type = account_type
        self.account_number = account_number
        self.account_balance = account_balance
    def display_all_accounts_of_user(self, accounts: list):
        for account in accounts:
            if isinstance(account, BankAccount):
                print(f"Account Number: {account.account_number}, Account Balance: {account.account_balance}")
            else:
                print("Invalid account object in the list.")
        
   

   