from aiogram import Router, F, types
import secrets
import sqlite3
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards import get_start_panel, get_confirm_title_panel
from aiogram.fsm.state import StatesGroup, State


router = Router()


CONN = sqlite3.connect("/app/bot_db/tg_bot_db.db")

CURSOR = CONN.cursor()

CURSOR.execute("""CREATE TABLE IF NOT EXISTS users (
               user_id INTEGER,
               password TEXT NOT NULL,
               created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               );""")


async def get_start_menu(event):

    if isinstance(event, types.CallbackQuery):
        await event.message.edit_text("Welcome to Oddities, bot for help you with content",
                reply_markup=get_start_panel())
    if isinstance(event, types.Message):
        await event.answer("Welcome to Oddities, bot for help you with content", reply_markup=get_start_panel(),
        )

    #await message.answer("Welcome to Oddities, bot for help you with content", reply_markup=get_start_panel(),
        #parse_mode="Markdown")


@router.message(Command("start"))
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
                await get_start_menu(message)
            elif response.status in [400, 409]:
                await get_start_menu(message)
            else:
                await message.answer(f"error in register ")

