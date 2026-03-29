from aiogram import Router, F, types
from aiogram.filters import Command
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from keyboards import get_start_panel, get_confirm_title_panel
from aiogram.fsm.state import StatesGroup, State
from handlers.start import get_start_menu
from handlers.titles import add_title
from handlers.titles import AddTitle
from keyboards import (get_base_add_panel, get_title_category_panel,
                       get_confirm_title_panel, get_title_fix_panel)


router = Router()

@router.callback_query(F.data == "to_start_menu")
async def to_start_menu(callback : types.CallbackQuery):
    await callback.answer()
    await get_start_menu(callback)

@router.callback_query(F.data == "to_back")
async def to_back(callback : types.CallbackQuery, state : FSMContext):
    datas = {

    }

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


