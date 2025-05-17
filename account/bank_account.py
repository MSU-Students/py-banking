import random

class BankAccount:
    def __init__(self, user_id, account_type, balance):
        self.user_id = user_id
        self.account_type = account_type
        self.balance = balance
        self.account_id = self.generate_account_id()

    def generate_account_id(self):
        return random.randint(100000, 999999)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.account_type,
            "balance": self.balance,
            "account_id": self.account_id
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            user_id=data["user_id"],
            account_type=data["account_type"],
            balance=data["balance"]
        )     
        account.account_id = data.get("account_id", account.generate_account_id())
        return account
