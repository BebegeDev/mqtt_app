import json
import os

import requests

current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\insolation.json"
print(project_root_path)
headers = {
    'accept': 'application/json',
}

params = {
    'orgId': '1',
    'var-station': 'mpei',
    'var-nwp_provider': 'icon',
}

response = requests.get('http://62.109.30.150:81/stations/mpei/icon', headers=headers)

if response.status_code == 200:  # Проверка успешного ответа (код 200 OK)
    try:
        json_data = response.json()  # Преобразование ответа в JSON

        with open(project_root_path, "w") as json_file:
            json.dump(json_data[:24], json_file)
    except ValueError:
        print("Сервер вернул некорректный JSON")
else:
    print(f"Запрос завершился с кодом ошибки {response.status_code}")
