from aiogram import Router, F, types
import os
import asyncio
import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards import (get_base_add_panel, get_category_panel,
                        get_watchlist_confirm_panel,get_watch_watchlist_panel
                        )
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal
from utils import push_to_history, delete_last, is_url_for_db
from datetime import datetime
from handlers.start import get_start_menu
from typing import Union

router = Router()

async def get_all_items(callback : types.CallbackQuery):
    url = "http://web:8000/api/watchlist/item"
    headers = {
        "X-Bot-Key": str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id": str(callback.from_user.id),
        "Content-Type": "application/json"
    }
    items = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                for item in data:
                    items[str(item['id'])] = {
                        'name': f"{item['name']}",
                        'year_start': f"{item['year_start']}"
                    }
        except Exception as e:
            print(e)
    return dict(reversed(list(items.items())))

async def get_item(event : Union[types.Message, types.CallbackQuery], item_id):
    url = f"http://web:8000/api/watchlist/item/{item_id}/"
    headers = {
        "X-Bot-Key": str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id": str(event.from_user.id),
        "Content-Type": "application/json"
    }
    item = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                item = await response.json()
        except Exception as e:
            print(e)


    text = f"{item['name']} |  {item.get('year_start')}  |  {item.get('category')}\n\n"

    """
            f"{item.get('synopsis', '')}\n\n"
            f"Director - {item.get('director', '')}\n"
            f"End Year = {item.get('year_end', '')}\n"
            f"Runtime - {item.get('runtime','')}\n"
            f"Seasons - {item.get('seasons', '')}\n"
            f"Episodes - {item.get('episodes', '')}\n\n"
            f"Note - {item.get('note', '')}\n"
            f"Link - {item.get('link', '')}"
    """
    if item['synopsis']:
        text += f"{item['synopsis']}\n\n"
    if item['director']:
        text += f"Director - {item['director']}\n"
    if item['year_end']:
        text += f"End Year - {item['year_end']}\n"
    if item['runtime']:
        text += f"Runtime - {item['runtime']}\n"
    if item['seasons']:
        text += f"Seasons - {item['director']}\n"
    if item['episodes']:
        text += f"Episodes - {item['episodes']}\n\n"
    if item['note']:
        text += f"Note - {item['note']}\n"
    if item['link']:
        text += f"Link - {item['link']}\n"



    # тут наверно надо сделать тему что в text вставялется доп инфа только если она есть
    # а если нет и не вставляется
    data = {
        'text' : text,
        'data' : item
    }
    return data


@router.callback_query(F.data == "open_watchlist")
async def watch_watchlist(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, 'WATCHLIST_WATCH_MENU_PAGE_0')

    items = await get_all_items(callback)
    await state.update_data(watchlist_data=items)
    # all_titles = titles
    await callback.message.edit_text("Watch Your Watchlist",
                                     reply_markup=get_watch_watchlist_panel(items),
                                     parse_mode="HTML",
                                     disable_web_page_preview=True
                                     )

@router.callback_query(F.data.contains("open_watchlist_page_"))
async def response_next_watchlist_page(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    page = int(callback.data.split("_")[3])

    await push_to_history(state, f'WATCHLIST_WATCH_MENU_PAGE_{page}')
    data = await state.get_data()
    items = data.get('watchlist_data')

    await callback.message.edit_text(
        f"Page {page + 1}",
        reply_markup=get_watch_watchlist_panel(items, page=page)
    )

@router.callback_query(F.data.contains("open_item_"))
async def open_item(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    item_id = int(callback.data.split("_")[2])
    await state.update_data(item_id=item_id)
    page = int(callback.data.split("_")[4])
    await push_to_history(state, f"WATCHLIST_WATCH_MENU_PAGE_{page}")
    item = await get_item(callback, item_id)
    await callback.message.edit_text(item['text'], reply_markup=get_base_add_panel())