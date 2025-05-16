import random

class BankAccount:
    def __init__(self, user_id, account_type, balance):
        self.user_id = user_id
        self.account_type = account_type
        self.balance = balance
        # prvious account_id
        self.account_number = account_number
        self.account_type = account_type

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.account_type,
            "balance": self.balance,
            "account_number": self.account_number,
            "account_type" : self.account_type
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            user_id=data["user_id"],
            account_type=data["full_name"],
            balance=data["balance"]
        )     
        account.account_id = data.get("account_id", account.generate_account_id())
        return account
