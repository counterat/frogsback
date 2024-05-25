
import time
import json
import threading
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import html
from payments import cryptomus
import uuid
import jwt
import  uvicorn
import hmac
import hashlib
from fastapi import FastAPI, WebSocket, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import *
import fakeredis
import json
import urllib.parse
import json
from clever import  API_TOKEN
from te import  validate_initdata, verify_signature
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from clever import API_TOKEN
from fastapi.responses import JSONResponse
app = FastAPI()


@app.options("/{path:path}")
async def options_handler(path: str):
    # Возвращаем ответ с кодом 200 для запросов OPTIONS
    return JSONResponse(content={}, status_code=200)

def escape_telegram_markdown(text):
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '\\']
    for char in escape_chars:
        text = text.replace(char, f'\{char}')
    return text
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Использование fakeredis для имитации работы с Redis
redis_db = fakeredis.FakeStrictRedis()

MIN_WITHDRAW_AMOUNT = 0.35

# WebSocket endpoints
active_websockets: List[WebSocket] = []
scheduler = AsyncIOScheduler()
from decimal import Decimal, getcontext
getcontext().prec = 10
async def fetch_old_unpaid_purchases():

        async with async_session() as session:

            query = select(Purchases_FrogTON).where(Purchases_FrogTON.created_at+ timedelta(hours=6) <datetime.now() , Purchases_FrogTON.profit_given == False)
            result = await session.execute(query)
            purchases = result.scalars().all()
            for purchase in purchases:
                query_for_user = select(Users_FrogTON).where(Users_FrogTON.id == purchase.was_purchased_by_user_id)
                query_for_good = select(Goods_FrogTON).where(Goods_FrogTON.id == purchase.good_id)
                print(purchase.to_dict(), 'ahiles')
                result_good = await  session.execute(query_for_good)
                result = await session.execute(query_for_user)
                good = result_good.scalars().all()[0]
                user = result.scalars().all()[0]
                balances = user.balances
                balances[good.name] = {}
                print(balances, 'valancesss')
                num = decimal.Decimal(str(good.income))
                update_user_query = (
                    update(Users_FrogTON)
                    .where(Users_FrogTON.id == user.id)
                    .values(real_balance=user.real_balance+num, profit=user.profit+num, balances=balances)
                )
                await session.execute(update_user_query)
                await session.commit()
                await  broadcast_message(json.dumps({"eventname":'income_for_frog', "user":user.to_dict()}))



            if purchases:
                update_query = (
                update(Purchases_FrogTON)
                .where(Purchases_FrogTON.id.in_([purchase.id for purchase in purchases]))
                .values(profit_given=True)
            )
                await session.execute(update_query)

            # Коммитим изменения в базу данных
            await session.commit()




scheduler.add_job(fetch_old_unpaid_purchases, 'interval', seconds=5)  # Запуск каждые 6 часов
scheduler.start()
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            # Пример получения сообщения от клиента (можно опустить)
            data = await websocket.receive_text()

                # Отправка сообщения всем подключенным клиентам
            print('стороннего')
            await broadcast_message("Получен OK от стороннего сервера")
    except WebSocketDisconnect:
        active_websockets.remove(websocket)

async def broadcast_message(message: str):
    for ws in active_websockets:
        await ws.send_text(message)
@app.get('/')
async def buy_frog(request: Request):
    return '1'
@app.post('/make_payment')
async def make_payment(request: Request):
    try:


        data = await request.json()
        print(data)
        user_id =int( data.get('userId'))
        amount = data.get('amount')
        cryptocurrency = data.get('currency')
        network = None
        if cryptocurrency =='TON':
            network = 'TON'
        elif cryptocurrency == 'USDT':
            network = 'TRON'
        result = await  find_user_by_id(user_id)
        user = result
        order_id = await generate_unique_uuid()
        payment = cryptomus({
"amount": f"{amount}",
            "currency": f'TON',
            'to_currency': f'{cryptocurrency}',
            "network": f'{network}',
            "order_id": order_id,        
    'url_return': 'https://frogsback.yuriyzholtov.com',
            'url_callback': "https://frogsback.yuriyzholtov.com/payment",


        }, 'https://api.cryptomus.com/v1/payment')
        print(payment)
        if payment:
            result = await add_payment(user_id, float(amount), uuid=payment['result']['uuid'], status = payment['result']['status'], order_id = payment['result'][
                'order_id'],
                               address = payment['result']['address'], url = payment['result']['url'])
            rsp = result.to_dict()
            rsp['amount'] = payment['result']['payer_amount']
            return rsp
    except Exception as ex:
        print(ex)
        return HTTPException(403)
@app.post('/make_payout')
async def make_payout_handler(request:Request):
    try:
        data = await  request.json()
        print(data)
        sign = data['frog']
        payout_id = data['payout_id']
        if jwt.decode(sign, 'admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithms="HS256"):
            dct = jwt.decode(sign, 'admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithms="HS256")
            if not (dct['login'] == 'admin' and dct['password'] == 'DHICvBAAS0ue'):
                raise HTTPException(404)
        else:
            raise HTTPException(404)
        if True:
            payout = await make_payout(payout_id)
            response = cryptomus({
                'amount': str(payout.ton_amount),
                'currency': 'TON',
                'order_id': payout.order_id,
                'address': payout.address,
                'to_currency': 'TON',
                'is_subtract': True,
                'from_currency': 'USDT',
                'network': 'TON',
                'url_callback': 'https://host.yuriyzholtov.com/payout'
            }, 'https://api.cryptomus.com/v1/payout')
            if not response['state']:
                message_text = f'Вам одобрено заявку на вывод {payout.amount} долларов!'

                # Формируем URL для отправки сообщения
                send_message_url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

                # Параметры запроса
                params = {
                    'chat_id': payout.user_id,
                    'text': message_text
                }

                # Отправляем POST-запрос к API Telegram для отправки сообщения
                response = requests.post(send_message_url, json=params)
        return {'is_ok':True}

    except Exception as ex :
            print(ex)
            return HTTPException(404)
@app.post('/decline_payout')
async def decline_payout(request: Request):
    try:
        data = await  request.json()
        sign = data['frog']
        payout_id = data['payout_id']
        if jwt.decode(sign, 'admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithms="HS256"):
            dct = jwt.decode(sign, 'admin_keyyydfdfldlsf343543rgfgdf{"sds////ааЖЖЖЖЖа', algorithms="HS256")
            if not (dct['login'] == 'admin' and dct['password'] == 'DHICvBAAS0ue'):
                raise HTTPException(404)
        else:
            raise HTTPException(404)
        if True:
            await decline_payout_handl(int(payout_id))


    except Exception as ex:
        print(ex)
        return HTTPException(403)

@app.post('/request_payout')
async def request_payout_request(request: Request):
    try:
        data = await  request.json()
        user_id = data.get('userId')
        amount = float(data.get('amount'))
        address = data.get('address')
        user = await find_user_by_id(user_id)
        print(user.to_dict(), 'ress')
        if user:
            print(user.to_dict(), 'ress')
            print('Кабинаа')
            if user.real_balance >= amount and amount >= MIN_WITHDRAW_AMOUNT:
                print('Кабинаа')
                if data.get('sign'):
                    print(jwt.decode(data.get('sign'), "secret_key", algorithms="HS256"), 'sign')
                    print(jwt.decode(data.get('sign'), "secret_key", algorithms="HS256")['id'] == user.telegram_id, 'siiign')
                    if jwt.decode(data.get('sign'), "secret_key", algorithms="HS256")['id'] == user.telegram_id:

                        payout, user = await add_payout(user_id, amount, address)
                        url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
                        
                        for chat_id in [881704893, 6874159282]:
                            params = {
                            'chat_id': f"{chat_id}",
                                'parse_mode': 'Markdown',
                            'text': f"""
Вывод
[{user.name}](tg://user?id={escape_telegram_markdown(str(user.telegram_id))})
баланс юзера - {escape_telegram_markdown(str(user.real_balance))}
время создания аккаунта юзера - {escape_telegram_markdown(str(user.created_at))}
телеграм айди юзера - {escape_telegram_markdown(str(user.telegram_id))}
юзернейм - ` @{(user.username)}`

Время создания вывода  - {escape_telegram_markdown(str(datetime.now()))}
Адресс для вывода - `{(payout.address)}`
Сумма вывода - {payout.ton_amount}

  """

                        }
                            response = requests.post(url, json=params)
                            print(response.text, 'bydlo')
                        return user.to_dict()
        return HTTPException(403)
    except Exception as ex:
        print(ex)
        return HTTPException(403)
allowed_ip='91.227.144.54'
@app.post('/payment')
async def payment(request: Request):
    try:

        response = await request.json()
        client_ip = request.client.host
        if client_ip != allowed_ip:
            raise HTTPException(status_code=403, detail="Forbidden")
        uuid = response['uuid']
        
        print(response, 'letoooo')
        uuid = response['uuid']
        
        if 'test'  in response['txid']:
            print(response['txid'],'test'  in response['txid'])
            raise HTTPException(403)
        if response['status'] == 'paid'  or response['status'] == 'paid_over' :
                user = await succesful_payment(uuid, 'paid')
                if user:
                    d=  user.to_dict()
                    d['eventname'] = 'paid_invoice'

                    await broadcast_message(json.dumps(d))
                    return user.to_dict()

    except Exception as ex:
        return HTTPException(403)


isTest = False
@app.post('/authorize')
async def authorize_user(request: Request):

        if not isTest:
            data = await request.json()
            initdata = data['initdata']
            invit_code = data.get('invitCode')
            result = validate_initdata(initdata)
            if result:
                user_id = result['id']
            else:
                return HTTPException(403)
            user = await find_user_by_telegram_id(user_id)
            if user:
                return user.to_dict()
            else:
                userr = await add_user(result['id'],result['first_name'], result.get('username'),datetime.now(), invit_code)
                return userr.to_dict()

        """data = await request.json()
        print(data)
        username = data['username']
        telegram_id = data['telegram_id']
        first_name = data['first_name']
        user = await find_user_by_telegram_id(telegram_id)
        print(user, 'resulttttt')

        if user!=[]:
            return user.to_dict()
        else:
            user = await add_user(telegram_id, first_name, username, datetime.now())
            return user.to_dict()"""


@app.post('/buy_frog')
async def buy_frog(request: Request):
    try:
        data = await request.json()
        sign = data.get('sign')
        frog_id = data.get("frog_id")
        user_id = data.get("user_id")
        user = await find_user_by_id(user_id)

        if user.sign != sign:
            return HTTPException(403)

        result = await buy_frog_by_user(user_id, frog_id)
        
        if result == 'you already have this frog':
            return {'error_text': 'Вы уже купили жабу этого вида!'}
        elif result == 'not enough money':
            return {'error_text':"Недостаточно денег для приобретения жабы!"}
        print(result, ';;;sdsdadsads')
        return result.to_dict()
    except Exception as ex:
        print(ex)
        return HTTPException(403)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)


