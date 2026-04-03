import os
import asyncio
import aiohttp
from aiogram import Router, F, types
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

class AddTitle(StatesGroup):
    waiting_for_name = State()
    waiting_for_year_start = State()
    waiting_for_year_end = State()
    waiting_for_review = State()
    waiting_for_director = State()
    waiting_for_start_watch = State()
    waiting_for_end_watch = State()
    waiting_for_rating = State()


@router.callback_query(F.data == "add_title")
async def add_title(callback: types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "START_MENU")
    await callback.message.edit_text("Chose the title category",
        reply_markup=get_title_category_panel())

@router.callback_query(F.data.contains("title_category_"))
async def choose_category(callback: types.CallbackQuery, state : FSMContext):
    chosen_category = callback.data
    await callback.answer()
    await push_to_history(state, "TITLE_PANEL_ADD_CATEGORY")
    await state.update_data(title_category=chosen_category)
    await state.set_state(AddTitle.waiting_for_name)
    await callback.message.answer("Write the title's name",
        reply_markup=get_base_add_panel())

@router.message(AddTitle.waiting_for_name)
async def add_title_name(message : types.Message, state : FSMContext):
    title_name = message.text
    await push_to_history(state, "TITLE_STATE_WAITING_FOR_NAME")
    await state.update_data(title_name=title_name)
    await message.answer("Write title's start year", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_year_start)

@router.message(AddTitle.waiting_for_year_start)
async def add_start_year(message : types.Message, state : FSMContext):
    title_start_year = message.text

    try:
        Decimal(title_start_year)
    except Exception:
        await message.answer("write the correct year", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_year_start)
        return

    await push_to_history(state, "TITLE_STATE_WAITING_FOR_YEAR_START")
    await state.update_data(title_year_start=title_start_year)
    await message.answer("Write the review for title", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_review)

@router.message(AddTitle.waiting_for_review)
async def add_review(message : types.Message, state : FSMContext):
    title_review = message.text
    await push_to_history(state, "TITLE_STATE_WAITING_FOR_REVIEW")
    await state.update_data(title_review=title_review)
    await message.answer("write the rating for title", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_rating)

@router.message(AddTitle.waiting_for_rating)
async def add_rating(message : types.Message, state : FSMContext):
    title_rating = message.text
    try:
        rating = Decimal(title_rating.replace(",", "."))
        min_rating = Decimal("0.5")
        max_rating = Decimal("10")
        if rating % Decimal("0.5") == 0 and rating >= min_rating and rating <= max_rating:
            pass
        else:
            raise
    except Exception:
        await message.answer("write the correct rating from 0.5 to 10, for example 7 or 7.5",
                             reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_rating)
        return

    await push_to_history(state, "TITLE_STATE_WAITING_FOR_RATING")

    await state.update_data(title_rating=title_rating)
    await message.answer("check", reply_markup=get_confirm_title_panel())

@router.callback_query(F.data == "title_confirm_panel_fix")
async def run_fix_panel(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "CONFIRM_TITLE_PANEL")
    await callback.message.edit_text("fix panel", reply_markup=get_title_fix_panel())

@router.callback_query(F.data == "title_confirm_panel_status")
async def show_status_panel(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "CONFIRM_TITLE_PANEL")
    await callback.message.edit_text("status panel", reply_markup=get_title_status_panel())

@router.callback_query(F.data.contains("title_status_panel_"))
async def choose_status(callback: types.CallbackQuery, state : FSMContext):
    chosen_status = callback.data
    await callback.answer()
    await push_to_history(state, "TITLE_STATUS_PANEL")
    await state.update_data(title_status=chosen_status)
    await callback.message.edit_text("check", reply_markup=get_confirm_title_panel())

@router.callback_query(F.data == "title_confirm_panel_start_watch")
async def run_add_start_watch(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "CONFIRM_TITLE_PANEL")
    await callback.message.answer("write date of start watch (for example 21.01.2026)",
                    reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_start_watch)

@router.message(AddTitle.waiting_for_start_watch)
async def add_start_watch(message : types.Message, state : FSMContext):
    start_watch_date = message.text
    try:
        correct_date = datetime.strptime(start_watch_date, "%d.%m.%Y").date()
        await push_to_history(state, "TITLE_STATE_WAITING_FOR_START_WATCH")
        await state.update_data(title_start_watch=start_watch_date)
        await message.answer("check", reply_markup=get_confirm_title_panel())

    except Exception:
        await message.answer("write correct date dd.mm.yyyy for example 21.01.2026",
                    reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_start_watch)

@router.callback_query(F.data == "title_confirm_panel_end_watch")
async def run_add_end_watch(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "CONFIRM_TITLE_PANEL")
    await callback.message.answer("write date of end watch (for example 03.02.2026)",
                    reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_end_watch)

@router.message(AddTitle.waiting_for_end_watch)
async def add_end_watch(message : types.Message, state : FSMContext):
    end_watch_date = message.text
    try:
        correct_date = datetime.strptime(end_watch_date, "%d.%m.%Y").date()
        await push_to_history(state, "TITLE_STATE_WAITING_FOR_END_WATCH")
        await state.update_data(title_end_watch=end_watch_date)
        await message.answer("check", reply_markup=get_confirm_title_panel())

    except Exception:
        await message.answer("write correct date dd.mm.yyyy for example 11.04.2026",
                    reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_end_watch)

@router.callback_query(F.data == "title_fix_panel_director")
async def run_add_director (callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "TITLE_CONFIRM_PANEL_FIX")
    await callback.message.edit_text("Write the name of Director", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_director)

@router.message(AddTitle.waiting_for_director)
async def add_director(message : types.Message, state : FSMContext):
    director = message.text
    await push_to_history(state, "TITLE_STATE_WAITING_FOR_DIRECTOR")
    await state.update_data(title_director=director)
    await message.answer("fix panel", reply_markup=get_title_fix_panel())

@router.callback_query(F.data == "title_fix_panel_year_end")
async def run_add_year_end(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await push_to_history(state, "TITLE_CONFIRM_PANEL_FIX")
    await callback.message.edit_text("Write the title's end year",
                reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_year_end)

@router.message(AddTitle.waiting_for_year_end)
async def add_year_end(message : types.Message, state : FSMContext):
    year_end = message.text
    try:
        Decimal(year_end)
        await push_to_history(state, "TITLE_STATE_WAITING_FOR_YEAR_END")
        await state.update_data(title_year_end=year_end)
        await message.answer("fix panel", reply_markup=get_title_fix_panel())
    except Exception:
        await message.answer("Write the correct title's end year for example 1997",
                                         reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_year_end)

@router.callback_query(F.data == "confirm_panel_save")
async def save_title(callback : types.CallbackQuery, state : FSMContext):
    await callback.answer()

    categories = {
        "title_category_movie" : "MV",
        "title_category_series" : "SR",
        "title_category_anime" : "ANM",
        "title_category_cartoon" : "CRT",
        "title_category_video" : "VD",
        "title_category_legal_case" : "LG",
        "title_category_written_content" : "READ",
        "title_category_other" : "OTHER"
    }

    statuses = {
        "title_status_panel_DONE" : "DONE",
        "title_status_panel_DROPPED" : "DROP",
        "title_status_panel_REVISIT" : "RVS",
        "title_status_panel_WATCHING" : "WATCH"
    }

    state_data = await state.get_data()
    category = categories[state_data['title_category']]
    name = state_data['title_name']
    year_start = state_data['title_year_start']
    review = state_data['title_review']
    rating = state_data['title_rating']
    status = ""
    start_watch = ""
    end_watch = ""
    director = ""
    year_end = ""

    post_data = {
        "name": name,
        "year_start": int(year_start),
        #"year_end": year_end,
        "category": category,
        "review": review,
        "rating": rating
    }

    if 'title_status' in state_data:
        status = statuses[state_data['title_status']]
        post_data['status'] = status
    if 'title_start_watch' in state_data:
        date = datetime.strptime(str(state_data['title_start_watch']), '%d.%m.%Y').date()
        start_watch = date.strftime('%Y-%m-%d')
        post_data['start_watch'] = start_watch
    if 'title_end_watch' in state_data:
        date = datetime.strptime(str(state_data['title_end_watch']), '%d.%m.%Y').date()
        end_watch = date.strftime('%Y-%m-%d')
        post_data['end_watch'] = end_watch
    if 'title_director' in state_data:
        director = state_data['title_director']
        post_data['director'] = director
    if 'title_year_end' in state_data:
        year_end = int(state_data['title_year_end'])
        post_data['year_end'] = year_end

    url = "http://web:8000/api/titles/title/"


    headers = {
        "X-Bot-Key" : str(os.getenv("BOT_MASTER_KEY")),
        "X-Telegram-Id" : str(callback.from_user.id),
        "Content-Type": "application/json"
    }


    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=post_data) as response:
                if response.status in [200, 201]:
                    await state.clear()
                    await callback.message.edit_text("Title Saved")
                    await asyncio.sleep(3)
                    await get_start_menu(callback)
                else:
                    await callback.message.answer(f"error {await response.json()}")
        except Exception:
            await callback.message.answer("error", reply_markup=get_confirm_title_panel())


    #await callback.message.answer(f'{category} {name} {year_start} {review} {rating} {status}')





    # конце надо сохронить на серваке запись - отчистить state.get_data() - отправить на start_panel