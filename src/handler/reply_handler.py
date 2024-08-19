from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

from random import randint

from database.db_function import AsyncOrmFunction
from handler.callback_handler import CallbackDataUserId
import keybord.inline_keybord as in_key
from handler.geo_function import distance_geo

router_reply = Router()

@router_reply.message(F.text == 'Искать 🔍')
async def start_poisk_resume(message: Message, bot = Bot):
    a = 0
    while a != 1:
        result = await AsyncOrmFunction.select_user_full(message.from_user.id)
        list_resume = await AsyncOrmFunction.selects(message.from_user.id, result.resume.city, 
                                                    result.resume.age_max_preference, result.resume.age_min_preference, 
                                                    result.resume.gender_interes, result.resume.distance_preference)

        if list_resume == []:
            await message.answer('Для вас не нашлось подходящих кандидатов')
            a = a+1 
        else:
            resume = list_resume[randint(0, (len(list_resume)-1))]
            distance = distance_geo(resume.longitude, resume.latitude, result.resume.longitude, result.resume.latitude)
            if result.ban_list == []:
                if distance <= result.resume.distance_preference:
                    await message.answer('Будьте внимательны, вы можете стать жертвой мошенников')
                    await message.answer_video_note(video_note = resume.video)
                    await message.answer(text = f'<b><i>Имя: </i></b>{resume.fake_name}\n\
<b><i>Возраст: </i></b>{resume.age}\n\
<b><i>Город: </i></b>{resume.city}\n\
<b><i>Растояние до вас: </i></b>{int(distance)}км\n\
<b><i>Описание: </i></b>{resume.description}',
                            parse_mode = "HTML", 
                            reply_markup = in_key.create_keybord_resume(CallbackDataUserId(index = 'like', user_id = resume.user_id, resume_id = resume.id), 
                                                        CallbackDataUserId(index = 'message', user_id = resume.user_id, resume_id = resume.id), 
                                                        CallbackDataUserId(index = 'ban', user_id = resume.user_id, resume_id = resume.id),
                                                        CallbackDataUserId(index = 'report', user_id = resume.user_id, resume_id = resume.id)))
                    a = a+1
                else:
                    a = 0
            if result.ban_list != []:
                for index in range(len(result.ban_list)):
                    if resume.user_id == result.ban_list[index].ban_id:
                        a = 0
                    if resume.user_id != result.ban_list[index].ban_id:
                        if distance <= result.resume.distance_preference:
                            await message.answer('Будьте внимательны, вы можете стать жертвой мошенников')
                            await message.answer_video_note(video_note = resume.video)
                            await message.answer(text = f'<b><i>Имя: </i></b>{resume.fake_name}\n\
<b><i>Возраст: </i></b>{resume.age}\n\
<b><i>Город: </i></b>{resume.city}\n\
<b><i>Растояние до вас: </i></b>{int(distance)}км\n\
<b><i>Описание: </i></b>{resume.description}',
                            parse_mode = "HTML", 
                            reply_markup = in_key.create_keybord_resume(CallbackDataUserId(index = 'like', user_id = resume.user_id, resume_id = resume.id), 
                                                        CallbackDataUserId(index = 'message', user_id = resume.user_id, resume_id = resume.id), 
                                                        CallbackDataUserId(index = 'ban', user_id = resume.user_id, resume_id = resume.id),
                                                        CallbackDataUserId(index = 'report', user_id = resume.user_id, resume_id = resume.id)))
                            a = a+1

@router_reply.message(F.text == 'Моя анкету 📝')
async def start_poisk_resume(message: Message):
    result = await AsyncOrmFunction.select_resume_user(message.from_user.id)

    if result.gender == 'man':
        gender_user = '💙'
    if result.gender == 'women':
        gender_user = '🩷'

    if result.gender_interes == 'man':
        gender_resume = '💙'
    if result.gender_interes == 'women':
        gender_resume = '🩷'

    await message.answer_video_note(video_note = result.video)
    await message.answer(text = f'<b><i>Имя: </i></b>{result.fake_name}\n\
<b><i>Возраст: </i></b>{result.age}\n\
<b><i>Город: </i></b>{result.city}\n\
<b><i>Ваш пол: </i></b>{gender_user}\n\
<b><i>Искомый пол: </i></b>{gender_resume}\n\
<b><i>Радиус поиска: </i></b>{result.distance_preference}\n\
<b><i>Возраст поиска: </i></b>{result.age_min_preference}-{result.age_max_preference}\n\
<b><i>Описание: </i></b>{result.description}',
    parse_mode = "HTML")

@router_reply.message(F.text == 'Настройки ⚙️')
async def start_poisk_resume(message: Message):
    await message.answer('Здесь вы можете изменить свою анкету, выберите что вы хотите изменить 👇🏼', 
                         reply_markup = in_key.keybord_new_resume)