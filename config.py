from dotenv import load_dotenv, dotenv_values
from aiogram import Bot, Dispatcher

load_dotenv()

config = dotenv_values(".env")

bot = Bot(config['BOT_API_KEY'])
dp = Dispatcher(bot)