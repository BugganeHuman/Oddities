from aiogram import Router, F, types
import os
import aiohttp
from aiogram.fsm.context import FSMContext
from keyboards import (get_base_add_panel, get_title_category_panel,
                       get_confirm_title_panel, get_title_fix_panel,
                       get_title_status_panel)
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal
from utils import push_to_history
from datetime import datetime
from handlers.start import get_start_menu

router = Router()


@router.callback_query(F.data == "open_titles")
async def watch_titles(callback : types.CallbackQuery, state : FSMContext ):
    await callback.answer()
    await push_to_history(state, 'START_MENU')

    url_get_all_titles = "http://web:8000/api/titles/title/"
    headers = {
        "X-Bot-Key" : str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id" : str(callback.from_user.id),
        "Content-Type": "application/json"
    }
    titles = {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url_get_all_titles, headers=headers) as response:
                data = await response.json()
                for item in data:
                    titles[str(item['id'])] = {
                        'name' : f"{item['name']}",
                        'rating' : f"{item['rating']}"
                        }


        except Exception:
            await callback.message.edit_text("error, write me to fix this @His_Serene_Highness",
                reply_markup=get_base_add_panel())

        titles_text = ""
        for item in titles:
            print(item)
            print(type(item))
            url_title = f"http://web:8000/api/titles/title/{item}/"
            print("DEBAG URL TITLE  ",url_title)
            title_str = (
                f"<a href='{url_title}'>{titles[item]['name']}</a> |"
                f"<b>{titles[item]['rating']}</b>\n\n"
            )
            titles_text += title_str
            


        await callback.message.edit_text(titles_text,
                                         reply_markup=get_base_add_panel(),
                                         parse_mode="HTML",
                                         disable_web_page_preview=True)
