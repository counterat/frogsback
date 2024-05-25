import json
import hashlib
import base64

# Ключ API для платежей
api_payment_key = 'mHc0WYZGw4dK67nkkHkkUbFv8mVWzUxFdN8HU5yU7DOOQ95iSmMAZ0fq5Ld00h1CpjA3es4AzCQ4LZYqenXnKhOcocln6zSaBO4B5zQVP9HEPRXwdGZ0tuscImdMkPjv'

# Данные платежа
data = {
    'type': 'payment',
    'uuid': 'e1830f1b-50fc-432e-80ec-15b58ccac867',
    'order_id': 'test_oNe6eIaSJpF1dkl',
    'amount': '1',
    'payment_amount': '1',
    'payment_amount_usd': '1',
    'merchant_amount': '1',
    'commission': '0',
    'is_final': True,
    'status': 'paid',
    'from': 'test_lxmaHovSJhBe20F',
    'wallet_address_uuid': None,
    'network': 'eth',
    'currency': 'ETH',
    'payer_currency': 'ETH',
    'payer_amount': '1',
    'payer_amount_exchange_rate': None,
    'additional_data': None,
    'transfer_id': None,
    'txid': 'test_3mKA4O9JRhdofyy',
    'sign': 'bbb77db90279770b83747dbbc03211ef'
}

# Извлекаем подпись и удаляем её из данных
sign = data.pop('sign')

# Кодирование данных в JSON, затем кодирование в base64 и конкатенация с ключом API
json_data = json.dumps(data, ensure_ascii=False)
base64_data = base64.b64encode(json_data.encode('utf-8')).decode('utf-8')
hash_input = base64_data + api_payment_key

# Генерация MD5-хеша
hash_output = hashlib.md5(hash_input.encode('utf-8')).hexdigest()

# Вывод хеша
print(hash_output)
print(sign)