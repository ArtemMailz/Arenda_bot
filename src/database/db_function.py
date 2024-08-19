from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.orm import joinedload, aliased, selectinload

from database.model import User, Resume, BanUser, LoveMessage
from conect_database import async_session

class AsyncOrmFunction():
    async def add_user(id_user: int):
        async with async_session() as session:
            
            '''
            Функция добавления пользователя в таблицу User
            '''

            qure = (
                insert(User)
                .values(user_id = id_user)
            )
            await session.execute(qure)
            await session.commit()
        
    async def select_user(id_user: int):
        async with async_session() as session:

            '''
            Функция проверяет зарегистрирован ли пользователь и имеет ли он резюме
            '''

            query = (
                select(User)
                .options(joinedload(User.resume))
                .filter(User.user_id == id_user)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()

            if result == []:
                return "no_regist"
            
            if result != []:
                if result[0].resume == None:
                    return "no_resume"
                if result[0].resume != None:
                    return "yes_resume"   
    
    async def add_resume(id_user: int, age: int, gender: str, gender_interes: str, city: str,
                            latitude: float, longitude: float, fake_name: str, description: str, video: str,
                            age_min_preference: int, age_max_preference: int, distance_preference: int):
        async with async_session() as session:

            '''
            Функция добавления нового резюме в таблицу Resume
            '''

            query = (
                insert(Resume)
                .values(
                    user_id = id_user,
                    age = age,
                    gender = gender,
                    gender_interes = gender_interes,
                    city = city,
                    latitude = latitude,
                    longitude = longitude,
                    fake_name = fake_name,
                    description = description,
                    video = video,
                    age_min_preference = age_min_preference,
                    age_max_preference = age_max_preference,
                    distance_preference = distance_preference
                )
            )      
            await session.execute(query)
            await session.commit()

    async def select_resume_user(id_user: int):
        async with async_session() as session:

            '''
            Функция выводит все данные резюме
            '''

            query = (
                select(Resume)
                .filter(Resume.user_id == id_user)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()

            return (result[0])
        
    async def selects(id_user: int, cite_user: str, age_max: int, age_min:int, gender_interes: str,
                      distance_user: int):
        async with async_session() as session:

            '''
            Функция выберает из таблицы Resume город, координаты, минимальный и максимальный возраст

            SELECT * FROM
	        (SELECT user_id, age, gender, city, latitude, longitude, fake_name
	        FROM public.resumes 
	        WHERE user_id!= 1742536734 and gender='women' and city='Raditsa-Krylovka' and age<=100 and age>=10) helper1
            WHERE age!=1000
            '''
            query = (
                select(Resume)
                .select_from(Resume)
                .filter(and_(Resume.user_id != id_user,
                             Resume.city == cite_user, 
                             Resume.age <= age_max, 
                             Resume.age >= age_min, 
                             Resume.gender == gender_interes,
                             Resume.distance_preference == distance_user
                             ))
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()

            return result

    async def upadate_name(id_user: int, new_name: str):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(fake_name = new_name)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_description(id_user: int, new_description: str):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(description = new_description)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_video(id_user: int, new_video: str):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(video = new_video)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_age(id_user: int, new_age: int):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(age = new_age)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_max_preference(id_user: int, new_max_preference: int):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(age_max_preference = new_max_preference)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_min_preference(id_user: int, new_min_preference: int):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(age_min_preference = new_min_preference)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_gender_interes(id_user: int, new_gender_interes: str):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(gender_interes = new_gender_interes)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_gender(id_user: int, new_gender: str):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(gender = new_gender)
            )

            await session.execute(query)
            await session.commit()

    async def upadate_distance(id_user: int, new_distance: int):
        async with async_session() as session:
            query = (
                update(Resume)
                .where(Resume.user_id == id_user)
                .values(distance_preference = new_distance)
            )

            await session.execute(query)
            await session.commit()

    async def select_user_full(id_user: int):
        async with async_session() as session:

            '''
            Функция проверяет зарегистрирован ли пользователь и имеет ли он резюме
            '''

            query = (
                select(User)
                .options(joinedload(User.resume), joinedload(User.ban_list))
                .filter(User.user_id == id_user)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()

            return result[0]
        
    async def add_ban_user(id_user: int, id_ban: int):
        async with async_session() as session:
            query = (
                insert(BanUser)
                .values(user_id = id_user,
                        ban_id = id_ban)
            )

            await session.execute(query)
            await session.commit()

    async def add_like_user(id_user: int, id_resume: int, message_love: str):
        async with async_session() as session:
            query = (
                insert(LoveMessage)
                .values(resume_id = id_resume,
                        sender_id = id_user,
                        message = message_love)
            )

            await session.execute(query)
            await session.commit()

    async def select_like_user(id_user: int, id_resume: int):
        async with async_session() as session:
            query = (
                select(LoveMessage)
                .filter(and_(LoveMessage.sender_id == id_user,
                             LoveMessage.resume_id == id_resume))
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()

            if result == []:
                return 'no_like'
            if result != []:
                if result[0].message == None:
                    return 'no_message'
                if result[0].message != None:
                    return 'message'
                
    async def upadate_message(id_user: int, id_resume: int, message_love: str):
        async with async_session() as session:
            query = (
                update(LoveMessage)
                .where(and_(LoveMessage.sender_id == id_user, 
                            LoveMessage.resume_id == id_resume))
                .values(message = message_love)
            )

            await session.execute(query)
            await session.commit()


    async def select_message_user(id_user: int, id_resume: int):
        async with async_session() as session:
            query = (
                select(LoveMessage.message) 
                .filter(and_(LoveMessage.sender_id == id_user,
                             LoveMessage.resume_id == id_resume))
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()
            return result[0]
        
    async def delete_resume(id_user: int):
        async with async_session() as session:
            query = (
                delete(Resume)
                .filter(Resume.user_id == id_user)
            )

            await session.execute(query)
            await session.commit()

    async def select_user_to_id(id_user: int):
        async with async_session() as session:

            query = (
                select(Resume)
                .filter(Resume.id == id_user)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()

            return result[0]
        
    async def select_full_user():
        async with async_session() as session:
            query = (
                select(User)
            )
            res = await session.execute(query)
            result = res.scalars().all()
            return result