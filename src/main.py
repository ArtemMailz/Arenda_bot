import asyncio
import logging
import os
import dotenv as dot

from aiogram import Bot, Dispatcher

from handler.callback_handler import router_callback
from handler.command_handler import routere_command

dot.load_dotenv('.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(f'{BOT_TOKEN}')
dp = Dispatcher()


async def main():
    dp.include_router(routere_command)
    dp.include_router(router_callback)
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')