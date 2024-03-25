import configparser

import pymysql
from pymysql.cursors import DictCursor

from utils.create_file_and_path import Util


def add_user():
    # Получаем данные пользователя из функции
    config = configparser.ConfigParser()
    config.read("utils/setting.ini")
    host = config['BD']['HOST']
    user = config['BD']['USER']
    password = config['BD']['PASSWORD']
    BD = config['BD']['BD_NAME']
    try:
        connect = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            cursorclass=DictCursor,
            database=BD,
            autocommit=True)

        return connect
    except Exception as e:
        print("Подключение не удалось")
        print(e)
        raise
