class BankAccount:
    user_id: int
    type: str  # saving
    balance: float

    def __init__(self, user_id: int, account_name: str, initial_balance: float = 0.0, account_type: str = "saving"):
        self.user_id = user_id
        self.account_name = account_name
        self.type = account_type
        self.balance = initial_balance

   