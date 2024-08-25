from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

import keybord.inline_keybord as in_key

routere_command = Router()

@routere_command.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет , в этом боте ты можешь подать обьявление о продажи, сдачи в аренду или о поиске недвижимости в Владивостоке\n\nЧто бы следить за новыми обьявлениями о продаже или аренде недвижимости, вам нужновступить в нашу 👉🏼 <a href="https://t.me/c/2185953665/6">группу</a> 👈🏼', reply_markup = in_key.keybord_anketa, parse_mode = 'HTML')
