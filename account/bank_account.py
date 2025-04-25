class BankAccount:
    user_id: int
    type: str  # saving
    balance: float

#account_number

    def __init__(self, user_id: str, account_number:int, initial_balance: float = 0.0, account_type: str = "saving"):
        self.user_id = user_id
        self.account_number = account_number
        #self.new name sa variable
        self.balance = initial_balance
        self.account_type = account_type
        
    


   