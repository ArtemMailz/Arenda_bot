from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData

import keybord.reply_keybord as re_key
import keybord.inline_keybord as in_key


router_callback = Router()

class CallbackDataUserId(CallbackData, prefix = "user"):
    user_id: int
    resume_id: int
    index: str

class ReportUser(StatesGroup):
    report_message = State()
    report_id_resume = State()


@router_callback.callback_query(F.data == 'start_resume')
async def proverka_pod(callback: CallbackQuery, state: FSMContext):
    pass

@router_callback.callback_query(CallbackDataUserId.filter())
async def ban_user(callback: CallbackQuery, callback_data: CallbackDataUserId):
    pass