from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from typing import Union


async def delete_last(state : FSMContext):
    data = await state.get_data()
    history = data.get('history', [])
    print(history)
    print("__________________DEBUG______________________")
    history.pop()
    await state.update_data(history=history)
    print(history)

async def push_to_history(state : FSMContext, screen_id : str):
    data = await state.get_data()
    history = data.get('history', [])
    history.append(screen_id)
    await state.update_data(history=history)


async def get_updated_title(event : Union[types.Message, types.CallbackQuery], state: FSMContext):
    from handlers.titles.watch_titles import get_title

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
    title_id = state_data.get('title_id')
    #data = await get_title(event, title_id)
    data = state_data.get('title_data')
    title = data['title_data']
    name = state_data.get("title_name", title['name'])
    review = state_data.get("title_review", title['review'])
    rating = state_data.get("title_rating", title['rating'])
    year_start = state_data.get("title_year_start", title['year_start'])
    year_end = state_data.get("title_year_end", title['year_end'])
    category = ""
    if "title_category" in state_data:
        category = categories[state_data["title_category"]]
    else:
        category = title['category']
    status = ""
    if "title_status" in state_data:
        status = statuses[state_data['title_status']]
    else:
        status = title['status']
    director = state_data.get("title_director", title['director'])
    start_watch = state_data.get("title_start_watch", title['start_watch'])
    end_watch = state_data.get("title_end_watch", title['end_watch'])
    print(title)

    text = (f"{name}  {year_start}\n"
            f"rating - {rating}\n\n"
            f"_____________________________________________________\n"
            f"{review}\n"
            f"_____________________________________________________\n\n"
            f"category - {category}\n"
            f"director - {director}\n"
            f"start watch - {start_watch}\n"
            f"end watch - {end_watch}\n"
            f"year_end - {year_end}\n"
            f"status - {status}"
            )



    #await state.update_data(title_data=t)
    """
    {'id': 18,
    'owner': 'The_EvilDog',
    'name': '3', 
    'year_start': 3,
    'year_end': None,
    'director': None, 
    'category': 'MV', 
    'cover': None, 
    'start_watch': None, 
    'end_watch': '2026-04-04', 
    'status': 'DONE', 
    'review': '3', 
    'rating': '3.0'}
    """

    return str(text)