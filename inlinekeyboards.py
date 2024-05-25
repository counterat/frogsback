from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
WEB_APP_URL = 'https://frogsfront.yuriyzholtov.com/'

def generate_start_kb(invit_code=''):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(  InlineKeyboardButton(text='Играть', web_app= WebAppInfo(url=WEB_APP_URL+str(invit_code))))
    return keyboard
def return_to_prev(msgKey):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Вернуть', callback_data=f'returnPrevMsg|{msgKey}'))
    return keyboard

inline_keyboards = {
    "start_message": lambda invitcode='': generate_start_kb(invitcode),
    "return_to_prev": lambda msgKey: return_to_prev(msgKey)

}

