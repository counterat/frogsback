import sys
print(sys.path)
from urllib.parse import parse_qs, unquote
import json
import hmac
import hashlib
from six import ensure_binary
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import binascii


# Пример использования

def validate_initdata(init_data_encoded):
    # Decode URL-encoded string
    init_data_decoded = unquote(init_data_encoded)

    # Parse query string into a dictionary
    query_params = parse_qs(init_data_decoded)

    # Extract the user JSON string
    user_json = query_params.get('user', [None])[0]
    if not user_json:
        print("User data not found")
        return

    # Load JSON data
    try:
        init_data = json.loads(user_json)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return

    # Extract and remove hash from the data if exists
    check_hash = init_data.get('hash')
    print(init_data)
    return init_data
    if 'hash' in init_data:
        del init_data['hash']

    # Create data check string
    data_check_string = '\n'.join(
        f"{key}={init_data[key]}" for key in sorted(init_data)
    )

    # Your bot token (keep it secure)
    bot_token = 'YOUR_BOT_TOKEN'

    # Calculate the hash
    expected_hash = hmac.new(
        key=bot_token.encode(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if expected_hash == check_hash:
        print("Validation successful")
    else:
        print("Validation failed")


validate_initdata('query_id=AAG9v400AAAAAL2_jTRqUVjP&user=%7B%22id%22%3A881704893%2C%22first_name%22%3A%22Yuriy%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22yuriy_bsrb%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1715035665&hash=caec8f670100a03a44211d674d54bd02536aaee3ecc6cc13242af60b807bcb55')
import json
from merkle_json import MerkleJson

mj = MerkleJson()

import base64
class InvalidHashException(Exception):
    pass


import hashlib

def generate_md5_hash(input_string):
    """
    Функция для генерации MD5 хэша из строки с использованием UTF-8 кодировки.
    Хэш будет идентичен тому, что генерируется в PHP.

    Args:
    input_string (str): Строка, для которой нужно вычислить хэш.

    Returns:
    str: Строковое представление MD5 хэша в шестнадцатеричном формате.
    """
    # Кодируем строку в UTF-8
    encoded_string = input_string.encode('utf-8')

    # Создаем MD5 хэш объект
    md5_hasher = hashlib.md5()

    # Подаем закодированную строку в хэшер
    md5_hasher.update(encoded_string)

    # Получаем хэш в шестнадцатеричном формате
    hex_dig = md5_hasher.hexdigest()

    return hex_dig
import requests

def get_md5_hash(text):
    # Формирование URL для API запроса
    api_url = "http://md5.jsontest.com/?text=" + text

    # Выполнение GET запроса к API
    response = requests.get(api_url)

    # Проверка на успешный ответ от API
    if response.status_code == 200:
        # Преобразование ответа из формата JSON
        data = response.json()
        # Возвращение MD5 хеша из ответа
        return data['md5']
    else:
        return "Ошибка при получении ответа от API"

secret_key = "mHc0WYZGw4dK67nkkHkkUbFv8mVWzUxFdN8HU5yU7DOOQ95iSmMAZ0fq5Ld00h1CpjA3es4AzCQ4LZYqenXnKhOcocln6zSaBO4B5zQVP9HEPRXwdGZ0tuscImdMkPjv"

def verify_signature(data,api_payment_key=secret_key):

        # Чтение данных из входного потока

        'data = json.loads(data)'
        print(api_payment_key)
        # Извлечение и удаление подписи из данных
        sign = data['sign']
        del data['sign']  # Удаляем подпись из данных для генерации новой подписи



        # Генерируем подпись: сначала кодируем данные в JSON, затем в base64, добавляем ключ и хешируем через MD5
        json_data = json.dumps(data,separators=(',', ':'))
       

        base64_encoded = base64.b64encode(json_data.encode())
        print('nnb', base64_encoded)
        print(base64_encoded.decode()+api_payment_key)
        """ digest.update((base64_encoded + secret_key.encode())) """
        if sign ==(generate_md5_hash(base64_encoded.decode()+secret_key)):
             print("true"*64)
             return  True
        print('false'*64)


       


import  datetime
print( datetime.datetime.now().__str__())



