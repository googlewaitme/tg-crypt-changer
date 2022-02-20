from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

from data import config
from utils.coin_api import CoinbaseApi


logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
coin_api = CoinbaseApi(config.COINBASE_API_KEY, config.COINBASE_API_SECRET)
