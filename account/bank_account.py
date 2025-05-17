import random
from collections import UserDict

class BankAccount:
    def __init__(self, user_id, full_name, balance, account_number, account_type: str,):
        self.user_id = user_id
        self.full_name = full_name
        self.balance = balance
        # prvious account_id
        self.account_number = account_number
        self.account_type = account_type


    def generate_account_number():
        return random.randint(100000, 999999)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "balance": self.balance,
            "account_number": self.account_number,
            "account_type" : self.account_type
        }

    @classmethod
    def from_dict(cls, data:UserDict):
        account = cls(
            user_id=data["user_id"],
            full_name=data.get("full_name", ""),
            balance=data.get("balance", 0),
            account_number=data.get("account_number"," "),
            account_type=data.get("account_type", "")
        )
        account.account_number = data.get("account_number", account.account_number)
        return account
