from math import ceil
from .api import CoinbaseApi


class BaseCurrency():
    def __init__(self, name: str,
                 long_name: str, currency_commission: int,
                 commission_procent: float, coin_api: CoinbaseApi,
                 resource_id: str):
        self.name = name
        self.long_name = long_name
        self.currency_commission = currency_commission
        self.commission_procent = commission_procent
        self.coin_api = coin_api
        self.resource_id = resource_id

    def check_wallet_adress(self, wallet_adress):
        return True

    def get_amounts(self, amount: int):
        currency_amount = None
        native_amount = None
        if 0.001 < amount < 2:
            currency_amount = amount
            native_amount = self.get_native_amount(amount)
        elif amount >= 300:
            native_amount = amount
            currency_amount = self.get_currency_amount(amount)
        return (currency_amount, native_amount)

    def get_resource(self):
        account = self.coin_api.get_account(self.resource_id)
        amount = round(float(account['balance']['amount']), 6)
        balance = f"{self.name} {amount}"
        return balance.ljust(15) + " : " + str(account['native_balance'])

    def get_native_amount(self, currency_amount):
        self.update_course()
        native_amount = self.now_course * currency_amount
        return native_amount

    def get_currency_amount(self, native_amount):
        self.update_course()
        currency_amount = native_amount / self.now_course
        currency_amount = round(currency_amount, 8)
        return currency_amount

    def update_course(self):
        self.now_course = self.coin_api.get_coin_price(self.name)

    def get_commision(self, count_of_rub):
        commission = max(100, ceil(count_of_rub * self.commission_procent))
        commission += self.currency_commission
        return commission
