import time

from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Request.command_operator import Command

mqttc = connection()
connect = add_user()
operator = Command(mqttc, connect)

b = []
while True:
    a = operator.get_excluded_engines()
    print(a)
    for i in a:
        if i not in b and i['available_dgu'] != -1:
            print(f"ДГУ №{i['slave']}")
        elif i['available_dgu'] == -1:
            print(f'ДГУ №{i['slave']} недоступен')
        else:
            print(f"ДГУ №{i['slave']} уже включен")
    b = a
    time.sleep(10)
