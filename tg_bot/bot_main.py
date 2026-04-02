import asyncio
from aiogram import Bot, Dispatcher
import os
from handlers import start, user, navigation
from handlers.titles import add_titles, watch_titles
from handlers.watchlist import watchlist

bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()


async def main():
    # Начинаем слушать сервера Телеграма (Polling)
    dp.include_router(start.router)
    dp.include_router(navigation.router)
    dp.include_router(add_titles.router)
    dp.include_router(watchlist.router)
    dp.include_router(user.router)
    dp.include_router(watch_titles.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
