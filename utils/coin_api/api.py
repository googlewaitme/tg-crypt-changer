from coinbase.wallet.client import Client


class CoinbaseApi:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_coin_price(self, crypt_currency='BTC', real_currency='RUB'):
        currency_pair = f"{crypt_currency}-{real_currency}"
        return self.client.get_buy_price(currency_pair=currency_pair)

    def get_current_user(self):
        return self.client.get_current_user()
