class BankAccount:
    user_id: int
    account_type: str
    account_number: str
    account_balance: float


    def __init__(self, user_id:int, account_type:str, account_number: str, account_balance: float = 0.0):
        self.user_id = user_id
        self.account_type = account_type
        self.account_number = account_number
        self.balance = account_balance
   

   