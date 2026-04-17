from aiogram import Router, F, types
import os
import asyncio
import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from celery.utils.functional import pass1
from keyboards import (get_base_add_panel, get_category_panel,
                        get_watchlist_confirm_panel, get_item_update_panel,
                        get_account_actions_panel)
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal
from utils import push_to_history, delete_last, is_url_for_db, get_updated_item
from datetime import datetime
from handlers.start import get_start_menu
import sqlite3


"""
функция me

функция показать пароль

изменить настройки кофиденциальности для вотчлиста/тайтлов

удалить аккаунт

"""
router = Router()

@router.callback_query(F.data == "account_actions")
async def show_account_actions(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "START_MENU")
    await callback.message.edit_text('Account actions', reply_markup=get_account_actions_panel())

@router.callback_query(F.data == "user_me")
async def show_user_info(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, 'SHOW_ACCOUNT_ACTIONS')

    url = "http://web:8000/api/users/me/"

    headers = {
        "X-Bot-Key" : str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id" : str(callback.from_user.id),
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    date_var = datetime.fromisoformat(data['date_joined'].replace('Z', '+00:00'))
                    date = date_var.strftime('%d.%m.%Y')
                    text = (f"ID - {data['id']}\n\n"
                            f"Username - {data['username']}\n\n"
                            f"Date joined - {date}")
                    await callback.message.edit_text(str(text), reply_markup=get_base_add_panel())
        except Exception as e:
            print(e)

@router.callback_query(F.data == "user_show_password")
async def show_password(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, 'SHOW_ACCOUNT_ACTIONS')
    user_id = callback.from_user.id
    CONN = sqlite3.connect("/app/bot_db/tg_bot_db.db")
    CURSOR = CONN.cursor()
    CURSOR.execute("SELECT password FROM users WHERE user_id = ?;", (user_id, ))
    data = CURSOR.fetchone()
    password = data[0]
    await callback.message.edit_text(f"<tg-spoiler><code>{password}</code></tg-spoiler>",
                                        parse_mode='HTML', reply_markup=get_base_add_panel())

@router.callback_query(F.data == 'user_toggle_visibility')
async def show_toggle_visibility(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
