"""Функции бота"""

import os

import asyncio
from dotenv import load_dotenv
import aiohttp
from pyrogram import Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup)

import config

load_dotenv()

POSTS_URL = os.getenv('POSTS_URL')


async def get_post_and_count(number: int) -> tuple[dict, int]:
    """Получаем из API пост по номеру и общее число постов"""

    async with aiohttp.ClientSession() as session:

        # Получаем JSON с постом по номеру
        post_task = asyncio.ensure_future(
            session.get(f'{POSTS_URL}/{number}')
        )

        # Получаем JSON со всеми постами
        all_posts_task = asyncio.ensure_future(
            session.get(POSTS_URL)
        )

        post_response, all_posts_response = await asyncio.gather(
            post_task,
            all_posts_task,
        )

        post = await post_response.json()
        all_posts = await all_posts_response.json()

    return post, len(all_posts)


async def update_post(app: Client, chat_id: int,
                      message_id: int, number: int = 1) -> None:
    """Создаем пост и обновляем его содержание"""

    keyboard = []
    post, all_posts_count = await get_post_and_count(number)

    formatted_post = await config.create_post_text(post, all_posts_count)


    # Граничное условие чтобы не выйти за нижний предел количества
    if number > 1:
        keyboard.append(InlineKeyboardButton(
            '👈',
            callback_data=str(number - 1)
        ))

    # Граничное условие чтобы не выйти за верхний предел количества
    if number < all_posts_count:
        keyboard.append(InlineKeyboardButton(
            '👉',
            callback_data=str(number + 1)
        ))


    # Награда для тех, кто дошел
    if number == 100:

        confetti = await app.send_message(chat_id, '🎉')
        await asyncio.sleep(5)
        await confetti.delete()

    await app.edit_message_text(
        chat_id, message_id,
        text=formatted_post,
        reply_markup=InlineKeyboardMarkup([keyboard])
    )
