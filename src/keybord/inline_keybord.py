from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

keybord_start = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = '🌟Заполнить анкету🌟', callback_data = 'start_resume')]
])

keybord_new_resume = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Имя', callback_data = 'update_name'),
    InlineKeyboardButton(text = 'Описание', callback_data = 'update_description'),
    InlineKeyboardButton(text = 'Видео', callback_data = 'update_video')],
    [InlineKeyboardButton(text = 'Возраст', callback_data = 'update_age'),
    InlineKeyboardButton(text = 'Min возраст', callback_data = 'update_min_age'),
    InlineKeyboardButton(text = 'Max возраст', callback_data = 'update_min_age')],
    [InlineKeyboardButton(text = 'Радиус поиска 🧭', callback_data = 'update_distance')],
    [InlineKeyboardButton(text = 'Пол', callback_data = 'update_gender'),
    InlineKeyboardButton(text = 'Искомый пол', callback_data = 'update_gender_interes')],
    [InlineKeyboardButton(text = '❌ Удалить анкету ❌', callback_data = 'delete_resume')]
])

keybord_delete = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Удалить 😮‍💨', callback_data = 'full_delete_resume'),
    InlineKeyboardButton(text = 'Отмена 🈚️', callback_data = 'no_delete_resume')]
])

def create_keybord_resume(callback_like, callback_message, callback_ban, callback_report):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Нравиться ❤️‍🔥', callback_data = callback_like)
    bulder.button(text = 'В бан 😈', callback_data = callback_ban)
    bulder.button(text = 'Оставить стикер 👻', callback_data = callback_message)
    bulder.button(text = 'Пожаловаться 👀', callback_data = callback_report)
    bulder.adjust(2)
    return bulder.as_markup()

def create_keybord_love_message(callback_yes, callback_no):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Показать ❤️', callback_data = callback_yes)
    bulder.button(text = 'Нет ❌', callback_data = callback_no)
    bulder.adjust(2)
    return bulder.as_markup()


def create_keybord_love_vz_message(callback_vz_love, callback_not):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Взаимно ❤️', callback_data = callback_vz_love)
    bulder.button(text = 'Не интересно❌', callback_data = callback_not)
    bulder.adjust(1)
    return bulder.as_markup()

def create_keybord_message(callback_love, callback_not):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Да ❤️', callback_data = callback_love)
    bulder.button(text = 'Нет ❌', callback_data = callback_not)
    bulder.adjust(1)
    return bulder.as_markup()

def create_keybord_report(callback_resume, callback_delete_report):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Показать анкету', callback_data = callback_resume)
    bulder.button(text = 'Удалить жалобу', callback_data = callback_delete_report)
    bulder.adjust(1)
    return bulder.as_markup()

def create_keybord_report_update(callback_resume_delete, callback_resume_skip):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = '❗️ Удалить анкету ❗️', callback_data = callback_resume_delete)
    bulder.button(text = 'Удалить жалобу', callback_data = callback_resume_skip)
    bulder.adjust(1)
    return bulder.as_markup()