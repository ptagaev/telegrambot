from bot import dp, bot, GROUP
from tables import User
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    message = State()


async def start_message_handler(message: types.Message, state: FSMContext):
    if state:
        await state.finish()
    User.add_user_to_database(message.from_user.id, message.from_user.username)

    await message.answer("hello")


async def join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    await bot.send_message(user_id, 'Реклама')
    User.add_user_to_database(update.from_user.id, update.from_user.username)
    await update.approve()


async def users_to_txt(message: types.Message):
    if message.chat.id == int(GROUP):
        User.users_to_txt()
        with open('users.txt', 'rb') as file:
            await message.answer_document(file, caption='База данных пользователей')


async def get_link(message: types.Message):
    # await message.answer(message.from_user.mention)
    if message.chat.id == int(GROUP):
        user_id = message.text.split(' ')[1]
        print(user_id)
        user_exist = User.user_exist(user_id)
        if user_exist:
            if user_exist.username:
                await message.answer('@' + user_exist.username)
            await message.answer(f'<a href="tg://user?id={int(user_id)}">ссылка</a>', parse_mode=types.ParseMode.HTML)
        else:
            await message.answer('такого пользователя нету')


async def sendall(message: types.Message):
    if message.chat.id == int(GROUP):
            text = message.text[9:]
            users = User.get_all()
            for row in users:
                try:
                    await bot.send_message(row, text)
                except:
                    continue
            await message.answer(f'Рассылка успешно прошла, количество пользователей {len(users)}')


async def count_user (message: types.Message):
    if message.chat.id == int(GROUP):
            users = User.get_all()
            await message.answer(f'Количество подписчиков {len(users)}')


async def recieve_post(message: types.Message):
    await FSMAdmin.message.set()
    await message.reply('Введите сообщение для рассылки')


async def admin_mail(message: types.Message, state:FSMContext):
    await state.finish()
    mail_message = await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)
    if message.chat.id == int(GROUP):
            users = User.get_all()
            for row in users:
                try:
                    await bot.send_message(row, mail_message)
                except:
                    continue
            await message.answer(f'Рассылка успешно прошла, количество пользователей {len(users)}')


def register_handler(dp: Dispatcher):
    dp.register_message_handler(start_message_handler, commands=["start"], state='*')
    dp.register_message_handler(users_to_txt, commands=['get_db'])
    dp.register_message_handler(get_link, commands=['get_link'])
    dp.register_chat_join_request_handler(join_request)
    dp.register_message_handler(recieve_post, commands=["sendall"])
    dp.register_message_handler(admin_mail, state=FSMAdmin.message, content_types=['any'])
    dp.register_message_handler(count_user, commands=["count_user"])
