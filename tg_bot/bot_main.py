import asyncio
from email.message import Message
import aiohttp
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import secrets
import sqlite3
from aiogram import F, types



CONN = sqlite3.connect("/app/bot_db/tg_bot_db.db")

CURSOR = CONN.cursor()

CURSOR.execute("""CREATE TABLE IF NOT EXISTS users (
               user_id INTEGER,
               password TEXT NOT NULL,
               created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               );""")


bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()

router = Router()


@dp.message(Command("start"))
async def start(message: types.Message):
    url = "http://web:8000/api/users/register/"

    user_password = secrets.token_hex(16)
    user_id = message.from_user.id

    CURSOR.execute("INSERT INTO users (user_id, password) VALUES (?, ?)",
            (user_id, user_password))

    data = {
        "username" : message.from_user.username,
        "telegram_id" : user_id,
        "password" : user_password,
        "email" : f"user_{user_id}@oddities.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status in [200, 201]:
                await message.answer("Hello you have been register")
            elif response.status in [400, 409]:
                await message.answer("Welcome back")
            else:
                await message.answer(f"error in register ")



async def main():
    # Начинаем слушать сервера Телеграма (Polling)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
