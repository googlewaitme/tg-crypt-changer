from math import ceil
from .api import CoinbaseApi
from data.config import states
from utils.db_api.models import CashArrival


class BaseCurrency():
    def __init__(self, name: str,
                 long_name: str, currency_commission: int,
                 coin_api: CoinbaseApi, resource_id: str):
        self.name = name
        self.long_name = long_name
        self.currency_commission = currency_commission
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

    def get_transactions(self, operation_type):
        if operation_type == 'buy':
            data = self.coin_api.get_buy_transactions(self.resource_id)
        else:
            data = self.coin_api.get_send_transactions(self.resource_id)
        text = "Транзакции💸\n"
        for transaction in data:
            text += self._make_text_from_transaction(transaction)
            if operation_type == 'buy':
                cash_arrival = CashArrival.get(transaction_id=transaction.id)
                operator_info = 'Информация о поступлении не указана🟥'
                if cash_arrival.is_operator_checked:
                    operator_info = "Указана новая информация🟩"
                text += "\n" + operator_info
                text += f"\nОценка в рублях: {cash_arrival.native_amount}"
            text += '\n-----\n'
        return text

    def _make_text_from_transaction(self, transaction):
        text = '\n' + transaction['details']['header']
        text += '\nСтатус: ' + transaction['status']
        if 'to' in transaction:
            text += '\nКошелёк: ' + transaction['to']['address']
        text += '\nДата: ' + transaction['created_at']
        return text

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

    def get_commision(self, count_of_rub, procent=None):
        if procent is None:
            procent = states['procent']
        commission = max(100, ceil(count_of_rub * procent / 100))
        commission += self.currency_commission
        return commission

    def update_cash_arrival(self, id, **params):
        query = CashArrival.update(**params).where(CashArrival.id == id)
        query.execute()

    def get_cash_arrival_which_operator_not_checked(self):
        cash_arrival = CashArrival.get_or_none(
            currency_name=self.name,
            is_operator_checked=False)
        return cash_arrival
