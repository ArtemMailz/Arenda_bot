from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

keybord_new_resume = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Имя', callback_data = 'update_name'),
    InlineKeyboardButton(text = 'Описание', callback_data = 'update_description'),
    InlineKeyboardButton(text = 'Видео', callback_data = 'update_video')]
])

def create_keybord_resume(callback_like):
    bulder = InlineKeyboardBuilder()
    bulder.button(text = 'Нравиться ❤️‍🔥', callback_data = callback_like)
    bulder.adjust(2)
    return bulder.as_markup()
