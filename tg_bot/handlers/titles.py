from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards import get_base_add_panel
from aiogram.fsm.state import StatesGroup, State


router = Router()

class AddTitle(StatesGroup):
    waiting_for_name = State()
    waiting_for_year = State()


@router.callback_query(F.data == "add_title")
async def add_title(callback: types.CallbackQuery, state : FSMContext):
    await callback.answer()
    await callback.message.edit_text("Write the title's name",
        reply_markup=get_base_add_panel())
    await state.set_state(AddTitle.waiting_for_name)


@router.message(AddTitle.waiting_for_name)
async def title_name_chosen(message : types.Message, state: FSMContext):
    title_name = message.text
    await state.update_data(title_name=title_name)
    await message.answer(f"your title is {title_name}")
    await state.clear()