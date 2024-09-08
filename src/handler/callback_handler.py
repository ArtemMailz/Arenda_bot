from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

import keybord.inline_keybord as in_key
import keybord.reply_keybord as re_key


router_callback = Router()

class CallbackDataUserId(CallbackData, prefix = "user"):
    user_id: int
    resume_id: int
    index: str

class Anketa_arend(StatesGroup):
    address = State()
    name_user = State()
    description = State()
    praice = State()
    image_1 = State()
    image_2 = State()
    image_3 = State()
    image_4 = State()
    image_5 = State()
    video_1 = State()
class Anketa_arend_pull(StatesGroup):
    address = State()
    name_user = State()
    description = State()
    username = State()
    praice = State()
    image_1 = State()
    image_2 = State()

@router_callback.callback_query(F.data == 'anketa_arenda')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, введите адресс вашего помещения \n\n\
Пример: г. Владивосток, р-он Первомайский, ул. Героев Хасана, д14')
    await state.set_state(Anketa_arend.address)

@router_callback.message(Anketa_arend.address)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Адрес записали, теперь укажите ваше имя\n\n\
Пример: Дмитрий', reply_markup = re_key.key_1)
    await state.update_data(address = message.text)
    await state.set_state(Anketa_arend.name_user)

@router_callback.message(Anketa_arend.name_user)
async def proverka_pod(message: Message, state: FSMContext):
    if message.text == 'Использовать ник 📝':
        await message.answer('Ваше имя записанно, теперь напишите описание к обьявлению\n\n\
Пример: Квартира сдаёться в хорошом состоянии, свежий ремонт, приятные соседи')
        await state.update_data(name_user = message.from_user.username)

    if message.text != 'Использовать ник 📝': 
        await message.answer('Ваше имя записанно, теперь напишите описание к обьявлению\n\n\
Пример: Квартира сдаёться в хорошом состоянии, свежий ремонт, приятные соседи')
        await state.update_data(name_user = message.from_user.username)

    await state.set_state(Anketa_arend.description)

@router_callback.message(Anketa_arend.description)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Описание добавленно, теперь укажите цену\n\n\
Пример: 55.000р/мес или 15.000р/м2 или 15.000.000р (если цена запокупку дома/квартиры полностью)')
    await state.update_data(description = message.text)
    await state.set_state(Anketa_arend.praice)

@router_callback.message(Anketa_arend.praice)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Теперь нужно загрузить 5 фото вашего помещения и одно видео\n\n\
Фото нужно загружать по одному, можете прислать первое фото')
    await state.update_data(praice = message.text)
    await state.set_state(Anketa_arend.image_1)


@router_callback.message(Anketa_arend.image_1)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Первое фото загруженно')
    await state.update_data(image_1 = message.photo[0].file_id)
    await state.set_state(Anketa_arend.image_2)

@router_callback.message(Anketa_arend.image_2)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Второе фото загруженно')
    await state.update_data(image_2 = message.photo[0].file_id)
    await state.set_state(Anketa_arend.image_3)

@router_callback.message(Anketa_arend.image_3)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Третье фото загруженно')
    await state.update_data(image_3 = message.photo[0].file_id)
    await state.set_state(Anketa_arend.image_4)

@router_callback.message(Anketa_arend.image_4)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Четвёртое фото загруженно')
    await state.update_data(image_4 = message.photo[0].file_id)
    await state.set_state(Anketa_arend.image_5)

@router_callback.message(Anketa_arend.image_5)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Пятое фото загруженно, теперь прешлите видео')
    await state.update_data(image_5 = message.photo[0].file_id)
    await state.set_state(Anketa_arend.video_1)

@router_callback.message(Anketa_arend.video_1)
async def proverka_pod(message: Message, state: FSMContext):
    await state.update_data(video_1 = message.video.file_id)
    result = await state.get_data()

    media_list = [
    InputMediaPhoto(type = 'photo', media = result['image_1']),
    InputMediaPhoto(type = 'photo', media = result['image_2']),
    InputMediaPhoto(type = 'photo', media = result['image_3']),
    InputMediaPhoto(type = 'photo', media = result['image_4']),
    InputMediaPhoto(type = 'photo', media = result['image_5']),
    InputMediaVideo(type = 'video', media = result['video_1'], 
                    caption = f'''✨<b><i>Новое обьявление</i></b>✨\n📍<b>Адрес: </b>{result['address']}\n📍<b>Продавец: </b><a href = "https://t.me/{message.from_user.username}">{result['name_user']}</a>\n📍<b>Стоимость: </b>{result['praice']}\n📍<b>Описание: </b>{result['description']}''',
                    parse_mode = 'HTML')
                    ]
    await message.answer_media_group(media = media_list)
    await message.answer('Опубликовать обьявление ?', reply_markup = in_key.keybord_anketa_post)

@router_callback.callback_query(F.data == 'post')
async def proverka_pod(callback: CallbackQuery, state: FSMContext, bot = Bot):
    await callback.message.delete()
    result = await state.get_data()

    media_list = [
    InputMediaPhoto(type = 'photo', media = result['image_1']),
    InputMediaPhoto(type = 'photo', media = result['image_2']),
    InputMediaPhoto(type = 'photo', media = result['image_3']),
    InputMediaPhoto(type = 'photo', media = result['image_4']),
    InputMediaPhoto(type = 'photo', media = result['image_5']),
    InputMediaVideo(type = 'video', media = result['video_1'], 
                    caption = f'''✨<b><i>Новое обьявление</i></b>✨\n📍<b>Адрес: </b>{result['address']}\n📍<b>Продавец: </b><a href = "https://t.me/{callback.from_user.username}">{result['name_user']}</a>\n📍<b>Стоимость: </b>{result['praice']}\n📍<b>Описание: </b>{result['description']}''',
                    parse_mode = 'HTML')
                    ]
    await bot.send_media_group(chat_id = -1002185953665, media = media_list, reply_to_message_id = 19)
    await state.clear()

    await callback.message.answer('Ваше обьявление успешно опубликованно✅')

@router_callback.callback_query(F.data == 'no_post')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router_callback.callback_query(F.data == 'anketa_claim')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Хорошо, введите адрес района поиска\n\n\
Пример: г. Владивосток, р-он Первомайский')
    await state.set_state(Anketa_arend_pull.address)

@router_callback.message(Anketa_arend_pull.address)
async def proverka_pod(message: Message, state: FSMContext):
    await state.update_data(address = message.from_user.username)
    await message.answer('Адрес записали, теперь укажите ваше имя\n\n\
Пример: Дмитрий', reply_markup = re_key.key_1)

    await state.set_state(Anketa_arend_pull.name_user)

@router_callback.message(Anketa_arend_pull.name_user)
async def proverka_pod(message: Message, state: FSMContext):
    if message.text == 'Использовать ник 📝':
        await message.answer('Ваше имя записанно, теперь напишите описание к обьявлению\n\n\
Пример: Квартира сдаёться в хорошом состоянии, свежий ремонт, приятные соседи')
        await state.update_data(name_user = message.from_user.username)

    if message.text != 'Использовать ник 📝': 
        await message.answer('Ваше имя записанно, теперь напишите описание к обьявлению\n\n\
Пример: Квартира сдаёться в хорошом состоянии, свежий ремонт, приятные соседи')
        await state.update_data(name_user = message.from_user.username)

    await state.set_state(Anketa_arend_pull.description)

@router_callback.message(Anketa_arend_pull.description)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Описание добавленно, теперь укажите желаемую цену\n\n\
Пример: 55.000р/мес или 15.000р/м2')
    await state.update_data(description = message.text)
    await state.set_state(Anketa_arend_pull.praice)

@router_callback.message(Anketa_arend_pull.praice)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Теперь нужно загрузить 2 ваших фото \n\n\
Фото нужно загружать по одному, можете прислать первое фото')
    await state.update_data(praice = message.text)
    await state.set_state(Anketa_arend_pull.image_1)


@router_callback.message(Anketa_arend_pull.image_1)
async def proverka_pod(message: Message, state: FSMContext):
    await message.answer('Первое фото загруженно')
    await state.update_data(image_1 = message.photo[0].file_id)
    await state.set_state(Anketa_arend_pull.image_2)

@router_callback.message(Anketa_arend_pull.image_2)
async def proverka_pod(message: Message, state: FSMContext):
    await state.update_data(image_2 = message.photo[0].file_id)
    result = await state.get_data()

    media_list = [
    InputMediaPhoto(type = 'photo', media = result['image_1']),
    InputMediaPhoto(type = 'photo', media = result['image_2'], 
                    caption = f'''✨<b><i>Новый искатель</i></b>✨\n📍<b>Адрес поиска: </b>{result['address']}\n📍<b>Искатель: </b><a href = "https://t.me/{message.from_user.username}">{result['name_user']}</a>\n📍<b>Желаемая цена: </b>{result['praice']}\n📍<b>Описание: </b>{result['description']}''',
                    parse_mode = 'HTML')
                    ]
    await message.answer_media_group(media = media_list)
    await message.answer('Опубликовать обьявление ?', reply_markup = in_key.keybord_anketa_post_pull)

@router_callback.callback_query(F.data == 'post_pull')
async def proverka_pod(callback: CallbackQuery, state: FSMContext, bot = Bot):
    await callback.message.delete()
    result = await state.get_data()

    media_list = [
    InputMediaPhoto(type = 'photo', media = result['image_1']),
    InputMediaPhoto(type = 'photo', media = result['image_2'], 
                    caption = f'''✨<b><i>Новый искатель</i></b>✨\n📍<b>Адрес поиска: </b>{result['address']}\n📍<b>Искатель: </b><a href = "https://t.me/{callback.from_user.username}">{result['name_user']}</a>\n📍<b>Желаемая цена: </b>{result['praice']}\n📍<b>Описание: </b>{result['description']}''',
                    parse_mode = 'HTML')
                    ]
    await bot.send_media_group(chat_id = -1002185953665, media = media_list, reply_to_message_id = 21)
    await state.clear()

    await callback.message.answer('Ваше обьявление успешно опубликованно✅')

@router_callback.callback_query(F.data == 'no_post_pull')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
