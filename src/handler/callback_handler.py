from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

import keybord.reply_keybord as re_key
from database.db_function import AsyncOrmFunction
from handler.geo_function import reverseGeocode, distance_geo
import keybord.inline_keybord as in_key


router_callback = Router()

class CallbackDataUserId(CallbackData, prefix = "user"):
    user_id: int
    resume_id: int
    index: str

class CallbackDataLoveUser(CallbackData, prefix = "love"):
    love_id: int
    index: str

class CallbackDataUsername(CallbackData, prefix = "user_name"):
    username: str
    id_message: int
    index: str

class UserState(StatesGroup):
    name = State()
    age = State()
    gender = State()
    gender_interes = State()
    city = State()
    latitude = State()
    longitude = State()
    description = State()
    age_min_preference = State()
    age_max_preference = State()
    distance_preference = State() 
    video = State()

class NewResume(StatesGroup):
    new_name = State()
    new_description = State()
    new_video = State()
    new_age = State()
    new_max_preference = State()
    new_min_preference = State()
    new_gender_interes = State()
    new_gender = State()
    new_distance = State()

class MessageLove(StatesGroup):
    id_return = State()
    id_user = State()
    message = State()
    my_id = State()

class ReportUser(StatesGroup):
    report_message = State()
    report_id_resume = State()

class MessageToLove(CallbackData, prefix = "user_message"):
    id_resume: int
    id_user: int
    index: str

class ReportMessage(CallbackData, prefix = "users_message"):
    id_resume: int
    index: str

class DeleteReport(CallbackData, prefix = "delete_message"):
    id_user: int
    index: str

@router_callback.callback_query(F.data == 'start_resume')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Что бы мы могли подобрать для вас новых знакомых нужно создать свою анкету, начнем с вашего имени, отправьте мне имя для анкеты или воспользуйтесь кнопочкой 🍇',
    reply_markup = re_key.keybord_name)
    await state.set_state(UserState.name)

@router_callback.message(UserState.name)
async def regist_name(message: Message, state: FSMContext):
    if message.text == 'Использовать мой ник 🍇':
        await state.update_data(name = message.from_user.username)
        await message.answer('Теперь нужен ваш возраст🤭')
        await state.set_state(UserState.age)
    if message.text != 'Использовать мой ник 🍇':
        await state.update_data(name = message.text)
        await message.answer('Теперь нужен ваш возраст🤭')
        await state.set_state(UserState.age)

@router_callback.message(UserState.age)
async def regist_age(message: Message, state: FSMContext):
    await state.update_data(age = message.text)
    await message.answer('Выберите ваш пол 👇🏼', reply_markup = re_key.keybord_gender)
    await state.set_state(UserState.gender)

@router_callback.message(UserState.gender)
async def regist_gender(message: Message, state: FSMContext):
    if message.text == 'Мужчина 💙':
        await state.update_data(gender = 'man')
    if message.text == 'Девушка 🩷':
        await state.update_data(gender = 'women')
    await message.answer('Какой пол вас интересует 🫣', reply_markup = re_key.keybord_gender_interes)
    await state.set_state(UserState.gender_interes)

@router_callback.message(UserState.gender_interes)
async def regist_gender_interes(message: Message, state: FSMContext):
    if message.text == 'Мужской 💙':
        await state.update_data(gender_interes = 'man')
    if message.text == 'Женский 🩷':
        await state.update_data(gender_interes = 'women')
    await message.answer('Для удобного и точного поиска новых знакомых, вам необходимо передать вашу геопозицию, ваши данные будут в безопасности ⚙️', reply_markup = re_key.keybord_geo)
    await state.set_state(UserState.city)

@router_callback.message(UserState.city)
async def regist_city(message: Message, state: FSMContext, bot = Bot):
    await state.update_data(latitude = message.location.latitude)
    await state.update_data(longitude = message.location.longitude)
    mess = await bot.send_message(message.from_user.id, 'Бот использует вашу геолокацию ✅')
    await bot.pin_chat_message(message.from_user.id, message_id = mess.message_id)

    result = reverseGeocode((message.location.latitude, message.location.longitude))

    await state.update_data(city = result)
    await message.answer('Записали ваше местоположение, теперь оно в безопасности. Пора предумать описание для вашей анкеты 😉')
    await state.set_state(UserState.description)

@router_callback.message(UserState.description)
async def regist_description(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await message.answer('Описание готово, какой возраст для вас минимальный ?')
    await state.set_state(UserState.age_min_preference)

@router_callback.message(UserState.age_min_preference)
async def regist_age_min(message: Message, state: FSMContext):
    await state.update_data(age_min_preference = message.text)
    await message.answer('А какой максимальный ?')
    await state.set_state(UserState.age_max_preference)

@router_callback.message(UserState.age_max_preference)
async def regist_age_max(message: Message, state: FSMContext):
    await state.update_data(age_max_preference = message.text)
    await message.answer('Выберети радиус поиска 🧭', reply_markup = re_key.keybord_radius)
    await state.set_state(UserState.distance_preference)

@router_callback.message(UserState.distance_preference)
async def regist_distance(message: Message, state: FSMContext):
    if message.text == '5км':
        await state.update_data(distance_preference = '5')
    if message.text == '10км':
        await state.update_data(distance_preference = '10')
    if message.text == '20км':
        await state.update_data(distance_preference = '20')
    if message.text == '30км':
        await state.update_data(distance_preference = '30')
    await message.answer('Пора загрузить кружочек для вашей анкеты 📸')
    await state.set_state(UserState.video)

@router_callback.message(UserState.video)
async def regist_video(message: Message, state: FSMContext):
    await state.update_data(video = message.video_note.file_id)
    result = await state.get_data()
    await AsyncOrmFunction.add_resume(int(message.from_user.id), int(result['age']), result['gender'], result['gender_interes'], result['city'], 
                                    float(result['latitude']), float(result['longitude']), result['name'], result['description'], result['video'], 
                                    int(result['age_min_preference']), int(result['age_max_preference']), int(result['distance_preference']))
    await message.answer('Анкета оформлена, теперь вы можете преступить к поиску новых знакомств', reply_markup = re_key.keybord_poisk)
    await state.clear()


@router_callback.callback_query(F.data == 'update_name') #обновляет имя
async def new_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_name)
    await callback.message.answer('Введите новое имя')

@router_callback.message(NewResume.new_name)
async def regist_new_name(message: Message, state: FSMContext):
    await state.update_data(new_name = message.text)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_name(message.from_user.id, result['new_name'])
    await state.clear()
    await message.answer('Имя успешно измененно ')
    

@router_callback.callback_query(F.data == 'update_description') #обновляет описание
async def new_description(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_description)
    await callback.message.answer('Введите новое описание')

@router_callback.message(NewResume.new_description)
async def regist_new_description(message: Message, state: FSMContext):
    await state.update_data(new_description = message.text)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_description(message.from_user.id, result['new_description'])
    await state.clear()
    await message.answer('Описание успешно измененно ')


@router_callback.callback_query(F.data == 'update_video') #обновляет фото
async def new_photo(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_video)
    await callback.message.answer('Пришлите новый кружочек')

@router_callback.message(NewResume.new_video)
async def regist_new_photo(message: Message, state: FSMContext):
    await state.update_data(new_video = message.video_note.file_id)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_video(message.from_user.id, result['new_video'])
    await state.clear()
    await message.answer('Кружочек успешно изменен')


@router_callback.callback_query(F.data == 'update_age') #обновляет возраст
async def new_age(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_age)
    await callback.message.answer('Введите новый возраст')

@router_callback.message(NewResume.new_age)
async def regist_new_age(message: Message, state: FSMContext):
    await state.update_data(new_age = message.text)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_age(message.from_user.id, int(result['new_age']))
    await state.clear()
    await message.answer('Возраст успешно изменённ')


@router_callback.callback_query(F.data == 'update_max_age') #обновляет максимальный возраст
async def new_max_preference(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_max_preference)
    await callback.message.answer('Введите новый максимальный возраст')

@router_callback.message(NewResume.new_max_preference)
async def regist_new_max_preference(message: Message, state: FSMContext):
    await state.update_data(new_max_preference = message.text)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_max_preference(message.from_user.id, int(result['new_max_preference']))
    await state.clear()
    await message.answer('Максимальный возраст успешно изменённ')


@router_callback.callback_query(F.data == 'update_min_age') #обновляет минимальный возраст
async def new_min_preference(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_min_preference)
    await callback.message.answer('Введите новый минимальный возраст')

@router_callback.message(NewResume.new_min_preference)
async def regist_new_min_preference(message: Message, state: FSMContext):
    await state.update_data(new_min_preference = message.text)
    result = await state.get_data()
    await AsyncOrmFunction.upadate_min_preference(message.from_user.id, int(result['new_min_preference']))
    await state.clear()
    await message.answer('Минимальный возраст успешно изменённ')


@router_callback.callback_query(F.data == 'update_distance') #обновляет дистанцию поиска
async def new_distance(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_distance)
    await callback.message.answer('Выберите новый радиус', reply_markup = re_key.keybord_radius)

@router_callback.message(NewResume.new_distance)
async def regist_new_distance(message: Message, state: FSMContext):
    if message.text == '5км':
        await state.update_data(new_distance = '5')
    if message.text == '10км':
        await state.update_data(new_distance = '10')
    if message.text == '20км':
        await state.update_data(new_distance = '20')
    if message.text == '30км':
        await state.update_data(new_distance = '30')
    result = await state.get_data()
    await AsyncOrmFunction.upadate_min_preference(message.from_user.id, int(result['new_distance']))
    await state.clear()
    await message.answer('Радиус поиска успешно изменённ')


@router_callback.callback_query(F.data == 'update_gender') #обновляет пол
async def new_gender(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_gender)
    await callback.message.answer('Выберите новый пол', reply_markup = re_key.keybord_gender)

@router_callback.message(NewResume.new_gender)
async def regist_new_gender(message: Message, state: FSMContext):
    if message.text == 'Мужчина 💙':
        await state.update_data(new_gender = 'man')
    if message.text == 'Девушка 🩷':
        await state.update_data(new_gender = 'women')
    result = await state.get_data()
    await AsyncOrmFunction.upadate_gender(message.from_user.id, result['new_gender'])
    await state.clear()
    await message.answer('Ваш пол успешно изменённ')


@router_callback.callback_query(F.data == 'update_gender_interes') #обновляет пол поиска
async def new_gender_interes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewResume.new_gender_interes)
    await callback.message.answer('Выберите новый пол для поиска', reply_markup = re_key.keybord_gender_interes)

@router_callback.message(NewResume.new_gender_interes)
async def regist_new_gender_interes(message: Message, state: FSMContext):
    if message.text == 'Мужской 💙':
        await state.update_data(new_gender_interes = 'man')
    if message.text == 'Женский 🩷':
        await state.update_data(new_gender_interes = 'women')
    result = await state.get_data()
    await AsyncOrmFunction.upadate_gender(message.from_user.id, result['new_gender_interes'])
    await state.clear()
    await message.answer('Пол поиска успешно изменённ')


@router_callback.callback_query(CallbackDataUserId.filter())
async def ban_user(callback: CallbackQuery, callback_data: CallbackDataUserId, state: FSMContext, bot = Bot):
    if callback_data.index == 'ban':
        await callback.message.delete()
        await AsyncOrmFunction.add_ban_user(callback.from_user.id, callback_data.user_id)
        await callback.answer('Пользователь занесен в черный список ✏️')

    if callback_data.index == 'message':
        await state.set_state(MessageLove.message)
        await state.update_data(id_resume = callback_data.resume_id) #айди резюме
        await state.update_data(id_user = callback_data.user_id) #айди пользователя резюме
        await state.update_data(id_messages = callback.from_user.id) #айди отправителя
        await callback.message.answer('Оставьте какой нибудь интересный стикер для этого пользователя 😉')

    if callback_data.index == 'like':
        message = await AsyncOrmFunction.select_like_user(callback.from_user.id, callback_data.resume_id)

        if message == 'no_like':
            user_id = callback.from_user.id
            await AsyncOrmFunction.add_like_user(callback.from_user.id, callback_data.resume_id, None)
            await bot.send_message(chat_id = callback_data.user_id, text = 'Ваша анкета кому-то понравилась, показать кому ?', 
                                   reply_markup = in_key.create_keybord_love_message(callback_yes = CallbackDataLoveUser(index = 'Yes', love_id = user_id),
                                                                                     callback_no = CallbackDataLoveUser(index = 'No', love_id = user_id)))
            await callback.message.answer('Ваша реация успешно отправлена ❣️')

        if message == 'no_message' and message == 'message':
            await callback.message.answer('Ваша реация уже была отправлена')

    if callback_data.index == 'report':
        await state.update_data(report_id_resume = callback_data.resume_id)
        await callback.message.answer('Укажите причину жалобы')
        await state.set_state(ReportUser.report_message)


@router_callback.message(ReportUser.report_message)
async def ban_user(message: Message, state: FSMContext,  bot = Bot):
    await state.update_data(report_message = message.text)
    report = await state.get_data()
    await message.answer('Ваша жалоба отправлена в службу поддержки 🤖')
    await bot.send_message(chat_id = '-1002242589305', text = f"На резюме №{report['report_id_resume']} была подана жалоба по причине: \n\n {report['report_message']}",
                           reply_markup = in_key.create_keybord_report(ReportMessage(index = 'resume', id_resume = report['report_id_resume']),
                                                                    ReportMessage(index = 'no', id_resume = report['report_id_resume'])))
    await state.clear()


@router_callback.message(MessageLove.message)
async def ban_user(message: Message, state: FSMContext,  bot = Bot):
    await state.update_data(message = message.sticker.file_id)
    result = await state.get_data()
    message_love = await AsyncOrmFunction.select_like_user(message.from_user.id, int(result['id_resume']))

    if message_love == 'no_like':
        await AsyncOrmFunction.add_like_user(message.from_user.id, int(result['id_resume']), result['message'])
        await bot.send_message(chat_id = int(result['id_user']), text = 'Вам отправили сообщение, посмотреть его 😳', 
                               reply_markup = in_key.create_keybord_message(MessageToLove(index = 'Yes', id_user = int(result['id_messages']), id_resume = int(result['id_resume'])),
                                                                                        MessageToLove(index = 'No', id_user = int(result['id_messages']), id_resume = int(result['id_resume']))))
        await message.answer('Ваше сообщение успешно отправленно')
        await state.clear()

    if message_love == 'no_message':
        await AsyncOrmFunction.upadate_message(message.from_user.id, int(result['id_resume']), result['message'])
        await bot.send_message(chat_id = int(result['id_user']), text = 'Вам отправили сообщение, посмотреть его 😳', 
                               reply_markup = in_key.create_keybord_message(MessageToLove(index = 'Yes', id_user = int(result['id_messages']), id_resume = int(result['id_resume'])),
                                                                                        MessageToLove(index = 'No', id_user = int(result['id_messages']), id_resume = int(result['id_resume']))))
        await message.answer('Ваше сообщение успешно отправленно')
        await state.clear()

    if message_love == 'message':
        await message.answer('Вы уже отправили сообщение')
        await state.clear()


@router_callback.callback_query(CallbackDataLoveUser.filter())
async def ban_user(callback: CallbackQuery, callback_data: CallbackDataLoveUser):
    if callback_data.index == 'Yes':
        resume_love = await AsyncOrmFunction.select_resume_user(callback_data.love_id)
        resume_user = await AsyncOrmFunction.select_resume_user(callback.from_user.id)
        distance = distance_geo(resume_love.longitude, resume_love.latitude, resume_user.longitude, resume_user.latitude)
        await callback.message.answer_photo(photo = resume_love.image, caption = f'<b><i>Имя: </i></b>{resume_love.fake_name}\n\
<b><i>Возраст: </i></b>{resume_love.age}\n\
<b><i>Город: </i></b>{resume_love.city}\n\
<b><i>Растояние до вас: </i></b>{int(distance)}км\n\
<b><i>Описание: </i></b>{resume_love.description}',
                    parse_mode = "HTML", 
                    reply_markup = in_key.create_keybord_love_vz_message(CallbackDataUsername(index = 'vz', id_message = resume_love.user_id, username = callback.from_user.username), 
                                                    CallbackDataUsername(index = 'no', id_message = resume_love.user_id, username = callback.from_user.username)))

    if callback_data.index == "No":
        await callback.message.delete()

@router_callback.callback_query(CallbackDataUsername.filter())
async def ban_user(callback: CallbackQuery, callback_data: CallbackDataUsername, bot = Bot):
    if callback_data.index == 'vz':
        await bot.send_message(chat_id = callback_data.id_message, text = f'У вас взаимные ❤️‍🔥\nМожете написать ему\ей @{callback_data.username}')
    if callback_data.index == 'no':
        await callback.message.delete()

@router_callback.callback_query(MessageToLove.filter())
async def ban_user(callback: CallbackQuery, callback_data: MessageToLove):
    if callback_data.index == 'Yes':
        result = await AsyncOrmFunction.select_message_user(callback_data.id_user, callback_data.id_resume)
        await callback.message.answer_sticker(sticker = result)
        await callback.message.answer(text = 'Что ответить пользователю ?', reply_markup = in_key.create_keybord_love_vz_message(CallbackDataUsername(index = 'vz', id_message = callback_data.id_user, username = callback.from_user.username), 
                                                    CallbackDataUsername(index = 'no', id_message = callback_data.id_user, username = callback.from_user.username)))
     
    if callback_data.index == 'No':
        callback.message.delete()




@router_callback.callback_query(F.data == 'delete_resume') #обновляет возраст
async def delete_resume(callback: CallbackQuery):
    await callback.message.answer('Вы уверены что хотите удалить свою анкету ?', reply_markup = in_key.keybord_delete)

@router_callback.callback_query(F.data == 'full_delete_resume') #обновляет возраст
async def full_delete_resume(callback: CallbackQuery):
    await AsyncOrmFunction.delete_resume(callback.from_user.id)
    await callback.message.answer('Анкета успешно удаленна 😔')

@router_callback.callback_query(F.data == 'no_delete_resume') #обновляет возраст
async def no_delete_resume(callback: CallbackQuery):
    await callback.message.delete()

@router_callback.callback_query(ReportMessage.filter())
async def ban_user(callback: CallbackQuery, callback_data: ReportMessage):
    if callback_data.index == 'no':
        await callback.message.delete()
    if callback_data.index == 'resume':
        result = await AsyncOrmFunction.select_user_to_id(int(callback_data.id_resume))
        await callback.message.delete()

        if result.gender == 'man':
            gender_user = '💙'
        if result.gender == 'women':
            gender_user = '🩷'

        if result.gender_interes == 'man':
            gender_resume = '💙'
        if result.gender_interes == 'women':
            gender_resume = '🩷'

        await callback.message.answer_video_note(video_note = result.video)
        await callback.message.answer(text = f'<b><i>Имя: </i></b>{result.fake_name}\n\
<b><i>Возраст: </i></b>{result.age}\n\
<b><i>Город: </i></b>{result.city}\n\
<b><i>Ваш пол: </i></b>{gender_user}\n\
<b><i>Искомый пол: </i></b>{gender_resume}\n\
<b><i>Радиус поиска: </i></b>{result.distance_preference}\n\
<b><i>Возраст поиска: </i></b>{result.age_min_preference}-{result.age_max_preference}\n\
<b><i>Описание: </i></b>{result.description}',
        parse_mode = "HTML",
        reply_markup = in_key.create_keybord_report_update(DeleteReport(id_user = result.user_id, index = 'delete'),
                                                           DeleteReport(id_user = result.user_id, index = 'no_delete')))
        
@router_callback.callback_query(DeleteReport.filter())
async def ban_user(callback: CallbackQuery, callback_data: DeleteReport):
    if callback_data.index == 'no_delete':
        await callback.message.delete()

    if callback_data.index == 'delete':
        await AsyncOrmFunction.delete_resume(callback_data.id_user)
        await callback.message.answer('Анкета удалена')