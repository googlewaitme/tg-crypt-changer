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

    def get_resurces(self):
        accounts = self.get_accounts()
        text = 'Остатки:\n'
        for account in accounts['data']:
            balance = str(account['balance'])
            native_balance = str(account['native_balance'])
            text += f"{balance} : {native_balance}\n"
        return text

    def send_money(self, transaction):
        resource_id = self.get_resource_id(transaction.currency_name)
        tx = self.client.send_money(
            resource_id,
            to=transaction.wallet_adress,
            amount=transaction.currency_count,
            idem=str(uuid.uuid4())
        )

    def get_current_user(self):
        return self.client.get_current_user()

    def get_accounts(self):
        return self.client.get_accounts()

    def get_resource_id(self, currency='BTC'):
        # TODO ME
        return 'lala'
