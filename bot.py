from aiogram import  Bot, Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

TOKEN = os.getenv('TOKEN')
GROUP = os.getenv('GROUP')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
