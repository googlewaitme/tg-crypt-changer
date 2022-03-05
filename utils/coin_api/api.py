from coinbase.wallet.client import Client
from datetime import datetime, timedelta
import uuid


class CoinbaseApi:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.bufer = dict()
        self.bufering_time = timedelta(minutes=18)

    def get_coin_price(self, base='BTC', currency='RUB'):
        request = f"{base}-{currency}"
        if request in self.bufer:
            delta_time = datetime.now() - self.bufer[request]['time']
            if delta_time <= self.bufering_time:
                return self.bufer[request]['price']
        row_price = self.client.get_buy_price(currency_pair=request)['amount']
        price = float(row_price)
        self.bufer[request] = {'price': price, 'time': datetime.now()}
        return price

    def _get_paginated_items(self, api_method, limit=300):
        """Generic getter for paginated items"""
        all_items = []
        starting_after = None
        while True:
            items = api_method(limit=limit, starting_after=starting_after)
            if items.pagination.next_starting_after is not None:
                starting_after = items.pagination.next_starting_after
                all_items += items.data
            else:
                all_items += items.data
                break
        return all_items

    def get_resurces(self):
        accounts = self.get_accounts()
        text = 'Остатки:\n'
        for account in accounts:
            balance = account['balance']
            native_balance = account['native_balance']
            if float(balance['amount']) > 0:
                text += f"{balance} : {native_balance}\n"
        return text

    def print_acount_info_by_name(self, name):
        accounts = self.get_accounts()
        for account in accounts:
            if name in account['currency']:
                print(account)

    def get_transactions(self, resource_id):
        return self.client.get_transactions(resource_id)['data']

    def get_account(self, resource_id):
        return self.client.get_account(resource_id)

    def send_money(self, transaction, currency):
        tx = self.client.send_money(
            currency.resource_id,
            currency=currency.name,
            to=transaction.wallet_adress,
            amount=transaction.currency_count,
            idem=str(uuid.uuid4())
        )

    def get_current_user(self):
        return self.client.get_current_user()

    def get_accounts(self):
        return self._get_paginated_items(api_method=self.client.get_accounts)
