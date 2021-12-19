from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.coin_api import CoinbaseApi

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
coin_api = CoinbaseApi(config.COINBASE_API_KEY, config.COINBASE_API_SECRET)
