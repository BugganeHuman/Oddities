from aiogram.fsm.context import FSMContext

async def push_to_history(state : FSMContext, screen_id : str):
    data = await state.get_data()
    history = data.get('history', [])
    history.append(screen_id)
    await state.update_data(history=history)