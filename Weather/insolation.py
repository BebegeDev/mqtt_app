import json
import os

import requests


class WeatherForecast:

    def __init__(self):
        self.params = None
        self.headers = None



    def __path_json_save(self):
        current_script_path = os.path.abspath(__file__)
        self.project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\insolation.json"


    def set_param(self, station='1', var_station='mpei', var_nwp_provider='icon'):
        self.headers = {
            'accept': 'application/json',
        }

        self.params = {
            'orgId': station,
            'var-station': var_station,
            'var-nwp_provider': var_nwp_provider,
        }


    def get_json(self):
        response = requests.get('http://62.109.30.150:81/stations/mpei/icon', headers=self.headers)
        if response.status_code == 200:  # Проверка успешного ответа (код 200 OK)
            try:
                json_data = response.json()  # Преобразование ответа в JSON

                with open(self.project_root_path, "w") as json_file:
                    json.dump(json_data[:24], json_file)
            except ValueError:
                print("Сервер вернул некорректный JSON")
        else:
            print(f"Запрос завершился с кодом ошибки {response.status_code}")
