from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

keybord_anketa = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Сдать\продать недвижимость', callback_data = 'anketa_arenda')],
    [InlineKeyboardButton(text = 'Купить\арендовать недвижимость', callback_data = 'anketa_claim')]
])

keybord_anketa_post = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Да', callback_data = 'post')],
    [InlineKeyboardButton(text = 'Нет', callback_data = 'no_post')]
])

keybord_anketa_post_pull = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Да', callback_data = 'post_pull')],
    [InlineKeyboardButton(text = 'Нет', callback_data = 'no_post_pull')]
])