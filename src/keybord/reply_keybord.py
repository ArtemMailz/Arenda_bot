from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keybord_name = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Использовать мой ник 🍇')]
], resize_keyboard = True)

keybord_gender = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Мужчина 💙'), 
    KeyboardButton(text = 'Девушка 🩷')]
], resize_keyboard = True)

keybord_gender_interes = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Мужской 💙'), 
    KeyboardButton(text = 'Женский 🩷')]
], resize_keyboard = True)

keybord_geo = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Передать геолокацию 📍', request_location = True)]
], resize_keyboard = True)

keybord_radius = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = '5км'), 
    KeyboardButton(text = '10км'),
    KeyboardButton(text = '20км'),
    KeyboardButton(text = '30км')]
], resize_keyboard = True)

keybord_poisk = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Искать 🔍'), 
    KeyboardButton(text = 'Моя анкету 📝')],
    [KeyboardButton(text = 'Настройки ⚙️')]
], resize_keyboard = True)