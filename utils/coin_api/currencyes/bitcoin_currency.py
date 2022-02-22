from utils.coin_api.base_currency import BaseCurrency


class BitcoinCurrency(BaseCurrency):
    def __init__(self, coin_api):
        super().__init__(
            name='BTC',
            long_name='bitcoin',
            currency_commission=40,
            commission_procent=0.1,
            coin_api=coin_api
        )