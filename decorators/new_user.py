import pymysql
from pymysql.cursors import DictCursor
from utils.create_file_and_path import Util


def new_user(func):
    def add_user(*args, **kwargs):
        # Получаем данные пользователя из функции
        user, password = func(*args, **kwargs)
        host = Util().config_pars('setting.ini')['DB']['HOST']

        try:
            # Устанавливаем соединение с базой данных
            with pymysql.connect(
                    host=host,
                    port=3306,
                    user=user,
                    password=password,
                    cursorclass=DictCursor
            ) as connection:
                print("Подключение к БД успешно")

                # Выполняем какие-то операции с базой данных
                with connection.cursor() as cursor:
                    cursor.execute("SHOW DATABASES;")
                    print(cursor.fetchall())

        except Exception as e:
            print("Подключение не удалось")
            print(e)
            raise

        # Возвращаем данные пользователя
        return user, password

    return add_user
