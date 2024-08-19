from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

import keybord.reply_keybord as re_key
import keybord.inline_keybord as in_key
from database.db_function import AsyncOrmFunction

from datetime import datetime
import time

routere_command = Router()

@routere_command.message(Command('test'))
async def start(message: Message):
    await AsyncOrmFunction.selects('Raditsa-Krylovka', 100, 10, 'women', 20)

@routere_command.message(Command('start'))
async def start(message: Message):

    if datetime.now().day == 16:
        await message.answer('red')

    result_regist = await AsyncOrmFunction.select_user(message.from_user.id)

    if result_regist == "no_regist":
        await AsyncOrmFunction.add_user(message.from_user.id)
        await message.answer(
        f'Привет <b>{message.from_user.first_name}</b> 👋🏻\n\n\
🌟 Готовы познакомиться с новыми людьми? Мы здесь, чтобы помочь вам найти интересных собеседников, друзей или даже спутника жизни!\n\
🔍 Просто расскажите нам немного о себе, своих интересах и ожиданиях, и мы подберем для вас подходящие варианты.\n\
💬 Наш бот предлагает удобный и анонимный способ общения. Вы можете общаться с потенциальными новыми знакомыми, не раскрывая свои личные данные, пока не будете готовы.\n\
🎉 Не теряйте времени, начните свое путешествие по новым знакомствам прямо сейчас!',
            parse_mode = "HTML",
            reply_markup = in_key.keybord_start) 

    if result_regist == "no_resume":
        await message.answer(
        f'Привет <b>{message.from_user.first_name}</b> 👋🏻\n\n\
🌟 Готовы познакомиться с новыми людьми? Мы здесь, чтобы помочь вам найти интересных собеседников, друзей или даже спутника жизни!\n\
🔍 Просто расскажите нам немного о себе, своих интересах и ожиданиях, и мы подберем для вас подходящие варианты.\n\
💬 Наш бот предлагает удобный и анонимный способ общения. Вы можете общаться с потенциальными новыми знакомыми, не раскрывая свои личные данные, пока не будете готовы.\n\
🎉 Не теряйте времени, начните свое путешествие по новым знакомствам прямо сейчас!',
            parse_mode = "HTML",
            reply_markup = in_key.keybord_start) 
        
    if result_regist == "yes_resume":
        await message.answer(
        f'Привет <b>{message.from_user.first_name}</b> 👋🏻\n\n\
Твоя анкета уже готова, вы можете начать искать новые знакомства прямо сейчас 💬',
        parse_mode = "HTML", 
        reply_markup = re_key.keybord_poisk) 
    