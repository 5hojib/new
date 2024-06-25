from os import environ
from logging import getLogger, basicConfig, ERROR, INFO
from pyrogram import Client

# Logging configuration
basicConfig(level=INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = getLogger(__name__)
getLogger("pyrogram").setLevel(ERROR)

# Admins
ADMINS = [2042193551, 5323651867]
MORE_ADMINS = list(map(int, environ.get('MORE_ADMINS', '').split()))
ADMINS.extend(MORE_ADMINS)

# Environment variables
APP_ID = environ['APP_ID']
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
DATABASE_URL = environ['DATABASE_URL']
STORE_CHANNEL = int(environ['STORE_CHANNEL'])


bot = Client('bot', APP_ID, API_HASH, bot_token = BOT_TOKEN).start()
BOT_NAME = bot.me.username
