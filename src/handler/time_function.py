from aiogram import Router
from aiogram.types import Message
from database.db_function import AsyncOrmFunction

time_router = Router()

async def time_message(bot):
    users = await AsyncOrmFunction.select_full_user()
    for index in range(0, len(users)-1):
        resumes = await AsyncOrmFunction.select_user_full(users[index].user_id)
        result_message = await AsyncOrmFunction.selects(users[index].user_id, resumes.resume.city, resumes.resume.age_max_preference, resumes.resume.age_min_preference, resumes.resume.gender_interes, resumes.resume.distance_preference)
        await bot.send_message(chat_id = users[index].user_id, text = f'Вы давно к нам не заходили, поблизости вас ожидают {len(result_message)} новых знакомств')
