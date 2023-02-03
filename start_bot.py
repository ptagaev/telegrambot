from aiogram import executor

from handlers import start_handler

from bot import dp

start_handler.register_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
