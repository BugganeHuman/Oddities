import asyncio
from email.message import Message
import aiohttp
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import secrets
import sqlite3

CONN = sqlite3.connect("/app/bot_db/tg_bot_db")

CURSOR = CONN.cursor()

CURSOR.execute("CREATE TABLE IF NOT EXIST users (username TEXT, password TEXT)")


bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()

router = Router()

"""
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(text=f"dick: {message.text}")
"""

from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command


@dp.message(F.text == "fuck u")
async def answer_to_hate(message: types.Message):
    await message.answer("no, u " + message.text)


#@dp.message(Command("start"))
@dp.message(F.text == "s")
async def start(message: types.Message):
    # тут надо регать юзера
    url = "http://web:8000/api/users/register"

    user_password = secrets.token_hex(16)

    data = {
        "username" : message.from_user.username,
        "tg_id" : message.from_user.id,
        "password" : user_password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            pass


    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            await message.answer(str(result))
    """

async def main():
    # Начинаем слушать сервера Телеграма (Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
