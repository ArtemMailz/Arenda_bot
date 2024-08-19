from sqlalchemy import Integer, String, ForeignKey, Text, LargeBinary, Float, BIGINT
from sqlalchemy.orm import relationship, Mapped, mapped_column

import enum
from typing import Optional, List

from conect_database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key = True)

    resume: Mapped[Optional["Resume"]] = relationship(back_populates = "users")
    ban_list: Mapped[List["BanUser"]] = relationship(back_populates = "user")

class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement = True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.user_id), )
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str]
    gender_interes: Mapped[str]
    city: Mapped[str] = mapped_column(String)
    latitude: Mapped[int] = mapped_column(Float)
    longitude: Mapped[int] = mapped_column(Float)
    fake_name: Mapped[int] = mapped_column(String)
    description: Mapped[int] = mapped_column(Text)
    video: Mapped[int] = mapped_column(String)
    age_min_preference: Mapped[int] = mapped_column(Integer)
    age_max_preference: Mapped[int] = mapped_column(Integer)
    distance_preference: Mapped[int] = mapped_column(Integer)

    users: Mapped["User"] = relationship(back_populates = "resume")
    love_messages: Mapped["LoveMessage"] = relationship(cascade='delete', back_populates = "resume_user")

class LoveMessage(Base):
    __tablename__ = "love_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    resume_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("resumes.id"))
    sender_id: Mapped[int] = mapped_column(BIGINT)
    message: Mapped[str] = mapped_column(Text, nullable = True)

    resume_user: Mapped["Resume"] = relationship(back_populates = "love_messages")

class BanUser(Base):
    __tablename__ = "users_ban"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.user_id))
    ban_id: Mapped[int] = mapped_column(BIGINT, primary_key = True)

    user: Mapped["User"] = relationship(back_populates = "ban_list")

# class AdminUser(Base):
#     __tablename__ = "admin_users"

#     admin_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.user_id))
#     give_id: Mapped[int] = mapped_column(BIGINT, primary_key = True)