from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

# ~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Главные штуки    ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("IP")  # Тоже str, но для айпи адреса хоста
COINBASE_API_SECRET = env.str('COINBASE_API_SECRET')
COINBASE_API_KEY = env.str('COINBASE_API_KEY')
# ~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Доп.штуки        ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~
URL_TO_RULES = env.str('URL_TO_RULES')
BOSS_ID = env.int('BOSS_ID')
URL_TO_BOSS = env.str('URL_TO_BOSS')
OPERATOR_ID = env.int('OPERATOR_ID')
URL_TO_OPERATOR = env.str('URL_TO_OPERATOR')
CARD_NUMBER = env.str('CARD_NUMBER')
# ~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~ Массивчики       ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~

CURRENCYES = ['BTC', "LTC"]
