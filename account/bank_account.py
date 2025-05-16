import random
from collections import UserDict

class BankAccount:
    def __init__(self, user_id, account_type, balance = 0, full_name = ''):
        self.user_id = user_id
        self.full_name = full_name
        self.balance = balance
        self.account_type = account_type
        self.account_id = self.generate_account_id()

    def generate_account_id(self):
        return random.randint(100000, 999999)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "account_type": self.account_type,
            "balance": self.balance,
            "account_id": self.account_id
        }

    @classmethod
    def from_dict(cls, data:UserDict):
        account = cls(
            user_id=data["user_id"],
            full_name=data.get("full_name", ""),
            balance=data.get("balance", 0),
            account_number=data.get("account_number"," "),
            account_type=data.get("account_type", ""),
            balance=data["balance"]
        )
        account.account_number = data.get("account_number", account.account_number)
        account.account_id = data.get("account_id", account.generate_account_id())
        return account
