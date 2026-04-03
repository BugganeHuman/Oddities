from aiogram import Router, F, types
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards import (get_start_panel, get_confirm_title_panel,
                       get_title_status_panel)
from aiogram.fsm.state import StatesGroup, State
from handlers.start import get_start_menu
from handlers.titles.add_titles import add_title
from handlers.titles.add_titles import AddTitle
from handlers.titles.watch_titles import get_all_titles, get_title
from keyboards import (get_base_add_panel, get_title_category_panel,
                       get_confirm_title_panel, get_title_fix_panel,
                       get_watch_titles_panel, get_open_title_panel)
from utils import push_to_history

router = Router()

@router.callback_query(F.data == "to_start_menu")
async def to_start_menu(callback : types.CallbackQuery):
    await callback.answer()
    await get_start_menu(callback)

@router.callback_query(F.data == "to_back")
async def to_back(callback : types.CallbackQuery, state : FSMContext):

    await callback.answer()
    data = await state.get_data()
    history = data.get('history')

    if not history:
        await to_start_menu(callback)
        return

    last_panel = history.pop()
    await state.update_data(history=history)

    if last_panel == "CONFIRM_TITLE_PANEL":
        await callback.message.edit_text("check", reply_markup=get_confirm_title_panel())
    elif last_panel == "TITLE_STATE_WAITING_FOR_RATING":
        await callback.message.answer("write the rating for title", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_rating)
    elif last_panel == "TITLE_STATE_WAITING_FOR_REVIEW":
        await callback.message.answer("Write the review for title", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_review)
    elif last_panel == "TITLE_STATE_WAITING_FOR_YEAR_START":
        await callback.message.answer("Write title's start year", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_year_start)
    elif last_panel == "TITLE_STATE_WAITING_FOR_NAME":
        await state.set_state(AddTitle.waiting_for_name)
        await callback.message.answer("Write the title's name",
                reply_markup=get_base_add_panel())
    elif last_panel == "TITLE_PANEL_ADD_CATEGORY":
        await callback.message.edit_text("Chose the title category",
                reply_markup=get_title_category_panel())
    elif last_panel == "START_MENU":
        await to_start_menu(callback)
    elif last_panel == "TITLE_STATUS_PANEL":
        await callback.message.edit_text("status panel", reply_markup=get_title_status_panel())
    elif last_panel == "TITLE_STATE_WAITING_FOR_START_WATCH":
        await callback.message.answer("write date of start watch (for example 21.01.2026)",
                                      reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_start_watch)
    elif last_panel == "TITLE_STATE_WAITING_FOR_END_WATCH":
        await callback.message.answer("write date of end watch (for example 03.02.2026)",
                                      reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_end_watch)
    elif last_panel == "TITLE_STATE_WAITING_FOR_DIRECTOR":
        await callback.message.answer("Write the name of Director", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_director)
    elif last_panel == "TITLE_CONFIRM_PANEL_FIX":
        await callback.message.edit_text("fix panel", reply_markup=get_title_fix_panel())
    elif last_panel == "TITLE_STATE_WAITING_FOR_YEAR_END":
        await callback.message.edit_text("Write the title's end year",
                                         reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_year_end)
    elif last_panel.startswith("TITLES_WATCH_MENU_PAGE_"):
        titles = await get_all_titles(callback)
        page = int(last_panel.split('_')[4])
        await callback.message.edit_text(
            f"Titles Page {page}",
            reply_markup=get_watch_titles_panel(titles, page=page)
        )
    elif last_panel.startswith("OPEN_TITLE_"):
        title_id = int(last_panel.split('_')[2])
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