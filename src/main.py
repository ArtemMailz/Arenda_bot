import asyncio
import logging
import os
import dotenv as dot

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handler.callback_handler import router_callback
from handler.command_handler import routere_command
from handler.reply_handler import router_reply
from handler.time_function import time_message

dot.load_dotenv('.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(f'{BOT_TOKEN}')
dp = Dispatcher()

sheduli = AsyncIOScheduler(timezone = "Europe/Moscow")

async def main():
    sheduli.add_job(time_message, trigger = 'interval', days = 2, args = [bot])
    sheduli.start()


    dp.include_router(routere_command)
    dp.include_router(router_callback)
    dp.include_router(router_reply)
    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot)
if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот остановлен')