from coinbase.wallet.client import Client
from datetime import datetime, timedelta


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
        price = self.client.get_buy_price(currency_pair=request)['amount']
        self.bufer[request] = {'price': price, 'time': datetime.now()}
        return price

    def get_current_user(self):
        return self.client.get_current_user()
