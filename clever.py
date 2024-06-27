import asyncio
import logging
from datetime import timedelta, datetime
import json

import jwt
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import *

import requests

from templatemessages import messages as templatemessages
from inlinekeyboards import inline_keyboards
admin_chat_id  = '881704893'

API_TOKEN = '7146421184:AAHx0S_cTcAd3JGSEn6yBhwKpMxNoLESR00'

logging.basicConfig(level=logging.INFO)
import threading
hostname = 'https://frogsback.yuriyzholtov.com'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
"""scheduler = AsyncIOScheduler()
scheduler.add_job(fetch_old_unpaid_purchases, 'interval', minutes=5)  # Запуск каждые 6 часов
scheduler.start()
"""
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    referal_code = message.get_args()
    if  not referal_code:
        referal_code = ''
    return await message.answer(templatemessages['start_message'](message.from_user.id, message.from_user.first_name), parse_mode=ParseMode.MARKDOWN,
                          reply_markup=inline_keyboards['start_message'](referal_code))
@dp.callback_query_handler(lambda query:   query.data.startswith('approve'))
async def approve_payout(query:types.CallbackQuery):

    data = {"frog" :jwt.encode({"login": "admin", "password": "DHICvBAAS0ue"}, key='admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithm="HS256"), 'payout_id':query.data.split(
        '_')[1]}
    response = requests.post(f'{hostname}/make_payout', json=data)
    await query.message.answer('00')
    await query.message.delete()

@dp.callback_query_handler(lambda query:   query.data.startswith('decline'))
async def decline_payout(query:types.CallbackQuery):
    data = {"frog": jwt.encode({"login": "admin", "password": "DHICvBAAS0ue"}, key='admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithm="HS256"),
            'payout_id': query.data.split(
                '_')[1]}
    response = requests.post(f'{hostname}/decline_payout', json=data)
    await query.message.answer('00')
    await query.message.delete()

@dp.callback_query_handler(lambda query:query.data=='howToPlay')
async def how_to_play_handler(query:types.CallbackQuery):

    await query.answer()
    return await query.message.edit_text(templatemessages['how_to_play'], parse_mode=ParseMode.MARKDOWN, reply_markup=inline_keyboards['return_to_prev']('start_message'))
@dp.callback_query_handler(lambda callback_query:callback_query.data.startswith('returnPrevMsg'))
async def return_to_prev_handler(query:types.CallbackQuery):
    prev_msg_key = query.data.split('|')[1]
    print(prev_msg_key)
    await query.message.edit_text(templatemessages[prev_msg_key](query.from_user.id, query.from_user.first_name), parse_mode=ParseMode.MARKDOWN)
    await  query.message.edit_reply_markup(inline_keyboards[prev_msg_key])
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    from aiogram import executor
    storage = MemoryStorage()
    # Подключаем MemoryStorage к боту
    dp.storage = storage
    executor.start_polling(dp, skip_updates=True)
