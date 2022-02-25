from utils.coin_api.base_currency import BaseCurrency
from data import config


class LitcoinCurrency(BaseCurrency):
    def __init__(self, coin_api):
        super().__init__(
            name='LTC',
            long_name='litcoin',
            currency_commission=20,
            commission_procent=0.1,
            coin_api=coin_api,
            resource_id=config.LTC_RESOURCE_ID
        )
