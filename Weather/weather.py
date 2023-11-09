import json
import os
from datetime import datetime
import requests
from sys import platform
import utils.open_json
import pandas as pd
from utils.create_file_and_path import Util


class WeatherForecast:

    def __init__(self):
        self.__params = None
        self.__headers = None
        self.set_param()
        self.__path_json_save()

    def __path_json_save(self):
        current_script_path = os.path.abspath(__file__)
        self.__project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\weather.json"

    def set_param(self, station='1', var_station='mpei', var_nwp_provider='icon'):
        self.__headers = {
            'accept': 'application/json',
        }

        self.__params = {
            'orgId': station,
            'var-station': var_station,
            'var-nwp_provider': var_nwp_provider,
        }

    def get_json(self):
        address = f"http://62.109.30.150:81/stations/" \
                  f"{self.__params['var-station']}/" \
                  f"{self.__params['var-nwp_provider']}"

        response = requests.get(address, headers=self.__headers)
        if response.status_code == 200:
            try:
                print(200)
                json_data = response.json()
                with open(self.__project_root_path, "w") as json_file:
                    data = self.__get_data()
                    json.dump(json_data[data:24+data], json_file)
            except ValueError:
                print("Сервер вернул некорректный JSON")
        else:
            print(f"Запрос завершился с кодом ошибки {response.status_code}")

    @staticmethod
    def __get_data():
        return int(datetime.now().strftime("%H"))
        
        
    @staticmethod
    def get_param_weather(hour=1, *param):
        data_json = Util().open_json("weather.json")
        if param:
            df = pd.json_normalize(data_json).iloc[hour].loc[list(param)]
        else:
            df = pd.json_normalize(data_json).iloc[hour]
        return df
