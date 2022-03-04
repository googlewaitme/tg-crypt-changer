from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

from utils.db_api.cashbox_api import CashboxApi
from utils.coin_api.currencyes import BitcoinCurrency, LitcoinCurrency
from utils.coin_api import CoinbaseApi
from data import config


logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
coin_api = CoinbaseApi(config.COINBASE_API_KEY, config.COINBASE_API_SECRET)
cashbox_api = CashboxApi()


get_currency = {
    'BTC': BitcoinCurrency(coin_api),
    'LTC': LitcoinCurrency(coin_api),
}

currencyes = get_currency.values()
