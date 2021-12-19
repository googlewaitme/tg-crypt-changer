from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("IP")  # Тоже str, но для айпи адреса хоста
COINBASE_API_SECRET = env.str('COINBASE_API_SECRET')
COINBASE_API_KEY = env.str('COINBASE_API_KEY')

CURRENCYES = ['BTC', "LTC"]
