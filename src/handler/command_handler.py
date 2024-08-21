from aiogram.types import Message
from aiogram import Router, Bot
from aiogram.filters import Command

import keybord.inline_keybord as in_key


#await bot.send_message(chat_id = -1002149371351, text = 'Link chat 1', reply_to_message_id = 1)
#await bot.send_message(chat_id = -1002149371351, text = 'Link chat 2', reply_to_message_id = 4)

routere_command = Router()

@routere_command.message(Command('start'))
async def start(message: Message):
    await message.answer(f'Привет , в этом боте ты можешь подать обьявление о продажи, сдачи в аренду или о поиске недвижимости в Владивостоке', reply_markup = in_key.keybord_anketa )
