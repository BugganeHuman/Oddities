from aiogram import Router, F, types
import os
import asyncio
import aiohttp
from aiogram.fsm.context import FSMContext
from keyboards import (get_base_add_panel, get_title_category_panel,
                       get_confirm_title_panel, get_title_fix_panel,
                       get_title_status_panel, get_watch_titles_panel,
                       get_open_title_panel, get_title_update_panel,
                       get_confirm_delete_panel)
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
    return dict(reversed(list(titles.items())))

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

    text = (f"{title['name']}  {title['year_start']}\n"
            f"rating - {title['rating']}\n\n"
            f"_____________________________________________________\n"
            f"{title['review']}\n"
            f"_____________________________________________________\n\n"
            f"category - {title['category']}\n"
            f"director - {title['director']}\n"
            f"start watch - {title['start_watch']}\n"
            f"end watch - {title['end_watch']}\n"
            f"year_end - {title['year_end']}\n"
            f"status - {title['status']}"
            )

    data = {
        'title_data' : title,
        'title_text' : text,
    }
    return data

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
        f"Page {page + 1}",
        reply_markup=get_watch_titles_panel(titles, page=page)
    )

@router.callback_query(F.data.contains('open_title_'))
async def watch_title(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    title_id = int(callback.data.split("_")[2])
    page = int(callback.data.split("_")[4])
    await push_to_history(state, f'TITLES_WATCH_MENU_PAGE_{page}')
    title = await get_title(callback, title_id)
    """
    text = (f"{title['name']}  {title['year_start']}\n"
            f"rating - {title['rating']}\n\n"
            f"_____________________________________________________\n"
            f"{title['review']}\n"
            f"_____________________________________________________\n\n"
            f"category - {title['category']}\n"
            f"director - {title['director']}\n"
            f"start watch - {title['start_watch']}\n"
            f"end watch - {title['end_watch']}\n"
            f"year_end - {title['year_end']}\n"
            f"status - {title['status']}"
            )
    """

    await callback.message.edit_text(title['title_text'], reply_markup=get_open_title_panel(title_id))

@router.callback_query(F.data.contains('confirm_delete_title_'))
async def run_confirm_delete(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    title_id = int(callback.data.split('_')[3])
    await push_to_history(state, F"OPEN_TITLE_{title_id}")
    await callback.message.edit_text('Are You Sure?',
        reply_markup=get_confirm_delete_panel(title_id))

@router.callback_query(F.data.contains('delete_title_'))
async def delete_title(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    title_id = int(callback.data.split('_')[2])
    url= f"http://web:8000/api/titles/title/{title_id}/"
    data = await state.get_data()
    pages = [key for key in data['history'] if key.startswith('TITLES_WATCH_MENU_PAGE_')]
    page = int(pages[-1].split('_')[4])
    headers = {
        "X-Bot-Key": str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id": str(callback.from_user.id),
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    await callback.message.edit_text('Title Have Deleted')
                    await asyncio.sleep(3)
                    await callback.message.edit_text(
                    f"Page {page}",
                        reply_markup=get_watch_titles_panel(await get_all_titles(callback), page=page)
                        )
                else:
                    print("status - ", response.status)
                    await callback.message.edit_text('delete error')
                    await asyncio.sleep(3)
                    await callback.message.edit_text(
                    f"Page {page}",
                        reply_markup=get_watch_titles_panel(await get_all_titles(callback), page=page)
                        )
        except Exception as e:
            print(e)

@router.callback_query(F.data.contains('update_title_'))
async def run_update(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    title_id = int(callback.data.split('_')[2])
    await push_to_history(state, F"OPEN_TITLE_{title_id}")
    await callback.message.edit_text("Update Title", reply_markup=get_title_update_panel())