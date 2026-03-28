from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards import get_base_add_panel, get_title_category_panel
from aiogram.fsm.state import StatesGroup, State
from decimal import Decimal

router = Router()

class AddTitle(StatesGroup):
    waiting_for_name = State()
    waiting_for_year_start = State()
    waiting_for_review = State()
    waiting_for_year_end = State()
    waiting_for_director = State()
    waiting_for_start_watch = State()
    waiting_for_end_watch = State()
    waiting_for_rating = State()


@router.callback_query(F.data == "add_title")
async def add_title(callback: types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.edit_text("Chose the title category",
        reply_markup=get_title_category_panel())

@router.callback_query(F.data.contains("title_category_"))
async def add_title_category(callback: types.CallbackQuery, state : FSMContext):
    chosen_category = callback.data
    await callback.answer()
    await state.update_data(category=chosen_category)
    await state.set_state(AddTitle.waiting_for_name)
    await callback.message.answer("Write the title's name",
        reply_markup=get_base_add_panel())

@router.message(AddTitle.waiting_for_name)
async def add_title_name(message : types.Message, state : FSMContext):
    title_name = message.text
    await state.update_data(title_name=title_name)
    await message.answer("Write title's start year", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_year_start)

@router.message(AddTitle.waiting_for_year_start)
async def add_start_year(message : types.Message, state : FSMContext):
    title_start_year = message.text

    if title_start_year.isdigit():
        pass
    else:
        await message.answer("write the correct year", reply_markup=get_base_add_panel())
        await state.set_state(AddTitle.waiting_for_year_start)
        return

    await state.update_data(title_start_year=title_start_year)
    #data = await state.get_data()
    await message.answer("Write the review for title", reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_review)

@router.message(AddTitle.waiting_for_review)
async def add_review(message : types.Message, state : FSMContext):
    title_review = message.text
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

    await state.update_data(title_rating=title_rating)
    await message.answer("check", reply_markup=get_base_add_panel())
