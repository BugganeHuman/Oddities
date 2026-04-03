from aiogram import Router, F, types
import os
import asyncio
import aiohttp
from aiogram.fsm.context import FSMContext
from keyboards import (get_base_add_panel, get_title_category_panel,
                       get_confirm_title_panel, get_title_fix_panel,
                       get_title_status_panel, get_watch_titles_panel,
                       get_open_title_panel)
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal
from utils import push_to_history
from datetime import datetime
from handlers.start import get_start_menu
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

all_titles = {}

async def get_all_titles(callback : types.CallbackQuery):
    url = "http://web:8000/api/titles/title/"
    headers = {
        "X-Bot-Key": str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id": str(callback.from_user.id),
        "Content-Type": "application/json"
    }
    titles = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                for item in data:
                    titles[str(item['id'])] = {
                        'name': f"{item['name']}",
                        'rating': f"{item['rating']}"
                    }
        except Exception as e:
            print(e)
    return titles

async def get_title(callback : types.CallbackQuery, title_id):
    url= f"http://web:8000/api/titles/title/{title_id}/"
    headers = {
        "X-Bot-Key": str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id": str(callback.from_user.id),
        "Content-Type": "application/json"
    }
    title = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                title = await response.json()
        except Exception as e:
            print(e)
    return title

@router.callback_query(F.data == "open_titles")
async def watch_titles(callback : types.CallbackQuery, state : FSMContext ):
    await callback.answer()
    await push_to_history(state, 'TITLES_WATCH_MENU_PAGE_0')

    # https://unconsecutively-polyprotic-fay.ngrok-free.dev

    titles = await get_all_titles(callback)
    #all_titles = titles
    await callback.message.edit_text("Watch Your Titles",
                                        reply_markup=get_watch_titles_panel(titles),
                                        parse_mode="HTML",
                                        disable_web_page_preview=True
                                        )


@router.callback_query(F.data.contains("open_titles_page_"))
async def response_next_titles_page(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    page = int(callback.data.split("_")[3])

    await push_to_history(state, f'TITLES_WATCH_MENU_PAGE_{page}')

    titles = await get_all_titles(callback)

    await callback.message.edit_text(
        f"Titles Page {page + 1}",
        reply_markup=get_watch_titles_panel(titles, page=page)
    )

@router.callback_query(F.data.contains('open_title_'))
async def watch_title(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    title_id = int(callback.data.split("_")[2])
    title = await get_title(callback, title_id)
    text = (f"{title['name']}\n"
            f"rating - {title['rating']}\n"
            f"{title['review']}")
    await callback.message.edit_text(text, reply_markup=get_open_title_panel())