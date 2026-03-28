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

def get_title_category_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text= "🎬 Movie", callback_data="title_category_movie")
    )
    builder.row(
        types.InlineKeyboardButton(text="📺 TV-Series", callback_data="title_category_series")
    )
    builder.row(
        types.InlineKeyboardButton(text="⛩️ Anime", callback_data="title_category_anime")
    )
    builder.row(
        types.InlineKeyboardButton(text="🎨 Cartoon", callback_data="title_category_cartoon")
    )
    builder.row(
        types.InlineKeyboardButton(text="🔴 Video",
                callback_data="title_category_video")
    )
    builder.row(
        types.InlineKeyboardButton(text="⚖️ Legal case", callback_data="title_category_legal_case")
    )
    builder.row(
        types.InlineKeyboardButton(text="📝 Written content", callback_data="title_category_written_content")
    )
    builder.row(
        types.InlineKeyboardButton(text="🌀 Other", callback_data="title_category_other")
    )

    builder.row(
        types.InlineKeyboardButton(text="🏠 Start Menu", callback_data="to_start_menu"),
        types.InlineKeyboardButton(text="⬅️ back", callback_data="to_back")
    )
    return builder.as_markup()



