from utils.coin_api.base_currency import BaseCurrency
from data import config


class LitcoinCurrency(BaseCurrency):
    def __init__(self, coin_api):
        super().__init__(
            name='LTC',
            long_name='litcoin',
            currency_commission=20,
            coin_api=coin_api,
            resource_id=config.LTC_RESOURCE_ID
        )

    def check_wallet_adress(self, wallet_adress):
        return wallet_adress[0] in 'ML3l' and len(wallet_adress) > 32
