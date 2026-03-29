import asyncio
from aiogram import Bot, Dispatcher
import os
from handlers import start, titles, watchlist, user, navigation


bot = Bot(token=os.getenv("BOT_TOKEN"))

dp = Dispatcher()


async def main():
    # Начинаем слушать сервера Телеграма (Polling)
    dp.include_router(start.router)
    dp.include_router(navigation.router)
    dp.include_router(titles.router)
    dp.include_router(watchlist.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
