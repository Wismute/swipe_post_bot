"""Бот просмотра постов"""

import os

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

import config
from main_functions import update_post

load_dotenv()

ACCOUNT = os.getenv('ACCOUNT')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

app = Client(
    name=ACCOUNT,
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


@app.on_message(filters.private & filters.command('start'))
async def start(_, message: Message):
    """Получение поста с кнопками для навигации"""

    await message.reply(
        config.HELLO_TEXT.format(message.from_user.first_name)
    )

    post = await message.reply('⌛️ Загрузка..')

    await update_post(app, message.chat.id, post.id)


@app.on_callback_query()
async def callback_buttons(_, update: CallbackQuery):
    """Получение и обработка данных из inline-кнопок"""

    await app.answer_callback_query(update.id)
    await update_post(app, update.message.chat.id,
                      update.message.id, int(update.data))


app.run()
