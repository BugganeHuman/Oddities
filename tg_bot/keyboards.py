from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder



def get_start_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text="📝 Add Title", callback_data="add_title"),
        types.InlineKeyboardButton(text="🗂️ Open Titles", callback_data="Open Titles")
    )

    builder.row(
        types.InlineKeyboardButton(text="📌 Add Watchlist Item", callback_data="Add Watchlist Item"),
        types.InlineKeyboardButton(text="🗒️ Open Watchlist", callback_data="Open Watchlist")
    )
    builder.row (
        types.InlineKeyboardButton(text="⚙️ Account Actions", callback_data="Account Actions")
    )

    return builder.as_markup()

def get_base_add_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text="🏠 Start Menu", callback_data="to_start_menu"),
        types.InlineKeyboardButton(text="⬅️ back", callback_data="to_back")
    )

    return builder.as_markup()