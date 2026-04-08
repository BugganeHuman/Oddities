from aiogram import Router, F, types
import os
import asyncio
import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards import (get_base_add_panel, get_category_panel,
                        get_watchlist_confirm_panel)
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal
from utils import push_to_history, delete_last
from datetime import datetime
from handlers.start import get_start_menu


router = Router()

class WatchlistState(StatesGroup):
    waiting_for_name = State()
    waiting_for_year_start = State()
    waiting_for_year_end = State()
    waiting_for_link = State()
    waiting_for_director = State()
    waiting_for_note = State()
    waiting_for_synopsis = State()
    waiting_for_runtime = State()
    waiting_for_episodes = State()
    waiting_for_seasons = State()

@router.callback_query(F.data == "add_watchlist_item")
async def add_watchlist_item(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await state.update_data(is_update=False)
    await push_to_history(state, "START_MENU")
    await callback.message.edit_text("Chose the item's category", reply_markup=get_category_panel('watchlist'))

@router.callback_query(F.data.contains('watchlist_category_'))
async def choose_item_category(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    categories = {
        "watchlist_category_movie" : "MV",
        "watchlist_category_series" : "SR",
        "watchlist_category_anime" : "ANM",
        "watchlist_category_cartoon" : "CRT",
        "watchlist_category_video" : "VD",
        "watchlist_category_legal_case" : "LG",
        "watchlist_category_written_content" : "READ",
        "watchlist_category_other" : "OTHER"
    }
    chosen_category = categories.get(callback.data, "OTHER")
    data = await state.get_data()
    is_update = data.get('is_update', False)
    await state.update_data(item_categoty=chosen_category)
    if is_update:
        pass
    else:
        await push_to_history(state, 'WATCHLIST_PANEL_ADD_CATEGORY')
        await state.set_state(WatchlistState.waiting_for_name)
        await callback.message.answer("Write the item's name",
            reply_markup=get_base_add_panel())

@router.message(WatchlistState.waiting_for_name)
async def add_item_name(message : types.Message, state : FSMContext):
    item_name = message.text
    data = await state.get_data()
    is_update = data.get('is_update', False)
    await state.update_data(item_name=item_name)
    if is_update:
        pass
    else:
        await push_to_history(state, 'WATCHLIST_STATE_WAITING_FOR_NAME')
        await message.answer("Write the start year of item",
                reply_markup=get_base_add_panel())
        await state.set_state(WatchlistState.waiting_for_year_start)

@router.message(WatchlistState.waiting_for_year_start)
async def add_item_year_start(message : types.Message, state : FSMContext):
    year_start = message.text
    data = await state.get_data()
    is_update = data.get('is_update', False)
    try:
        Decimal(year_start)
    except Exception:
        await message.answer('Write the correct year for example 1997', reply_markup=get_base_add_panel())
        await state.set_state(WatchlistState.waiting_for_year_start)
        return
    await state.update_data(item_year_start=year_start)
    if is_update:
        pass
    else:
        await push_to_history(state, 'WATCHLIST_STATE_WAITING_FOR_YEAR_START')
        await message.answer('confirm panel', reply_markup=get_watchlist_confirm_panel())