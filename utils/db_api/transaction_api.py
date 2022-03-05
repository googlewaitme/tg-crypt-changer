from .models import Transaction


class TransactionApi:
    def __init__(self):
        self.lala = True

    def create(self, **params):
        self.model = Transaction.create(**params)
        return self.model
