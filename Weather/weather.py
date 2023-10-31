import json
import os
from datetime import datetime
import requests
from sys import platform
import utils.open_json
import pandas as pd


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
                json_data = response.json()
                with open(self.__project_root_path, "w") as json_file:
                    self.__get_data()
                    json.dump(json_data[self.current_time:24+self.current_time], json_file)
            except ValueError:
                print("Сервер вернул некорректный JSON")
        else:
            print(f"Запрос завершился с кодом ошибки {response.status_code}")

    def __get_data(self):
        now = datetime.now()
        self.current_time = int(now.strftime("%H"))
        
        
    @staticmethod
    def get_param_weather(hour=1, *param):
        ob_json = utils.open_json.OpenJson()
        data_json = None
        if platform == 'win32' or platform == 'win64':
            data_json = ob_json.open_json('\\utils\\weather.json')
        elif platform == 'linux' or platform == 'linux2':
            data_json = ob_json.open_json('/utils/weather.json')
        if param:
            df = pd.json_normalize(data_json).iloc[hour].loc[list(param)]
        else:
            df = pd.json_normalize(data_json).iloc[hour]
        print(df)
        return df
