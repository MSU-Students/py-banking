
counter = 0
class BankAccount:
    user_id: int
    type: str #saving
    balance: float
    
    def __init__(self):
        global counter
        self.user_id = counter
        counter += 1