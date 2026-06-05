import requests

url = 'http://localhost/print'

payload = [
    {'type': 'text', 'content': '--- INTERNATIONAL CHAR TEST ---\n'},
    {'type': 'text', 'content': 'Cyrillic (Lower): абвгдеёжзийклмнопрстуфхцчшщъыьэюя\n'},
    {'type': 'text', 'content': 'Cyrillic (Upper): АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ\n'},
    {'type': 'text', 'content': '--- END TEST ---\n\n\n\n'}
]

try:
    print('Sending international character test...')
    response = requests.post(url, json=payload)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
