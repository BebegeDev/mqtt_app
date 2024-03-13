import asyncio
from Connected.contact_mqtt import connection
# from Connected.connection_db import DatabaseConnectionThread
from Diesel.diesel_command import DieselCommand
from Diesel.diesel_contact import DieselContact
from utils.create_file_and_path import Util
from utils.publish import Publish
from Emulators.emulators_contact import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Diesel.diesel_callback import DieselCallback
from Emulators.emulators_callback import EmCallback
from Victron.victron_contact import VictronCommand
from CommandOperator.command_operator import Command
from Connected.connection_db import add_user


def init_start():
    mqttc = connection()
    command_operator = Command(mqttc)
    command_operator.callback_data()
    while True:
        connect = add_user()
        if command_operator.check_connections(connect):
            asyncio.run(process_data(mqttc, command_operator))


async def process_data(mqttc, command_operator):
    print("START INIT")
    # подключение к ДБ
    connect = add_user()
    # Экземпляр класса Util
    data_path = Util()
    # экземпляр класса Publish
    publish = Publish(mqttc)
    # Создание экземпляра класса ContactEmulators
    emulators_contact_one = ContactEmulators("EM_ONE")
    # emulators_contact_two = ContactEmulators("EM_TWO")
    # подключение к дизелям
    # diesel_contact = DieselContact()
    # подключение к имитаторам
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    # emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))
    # создание экземпляра класса CommandEmulators
    emulators_command_one = CommandEmulators(emulators_contact_one)
    # emulators_command_two = CommandEmulators(emulators_contact_two)
    # создание экземпляра класса DieselCommand
    # diesel_command = DieselCommand(diesel_contact)
    # создание экземпляра класса EmCallback
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    # emulators_callback_two = EmCallback(mqttc, emulators_contact_two)
    # создание экземпляра класса DieselCallback
    # diesel_callback = DieselCallback(mqttc, diesel_command)
    # создание экземпляра класса VictronCommand
    victron = VictronCommand(mqttc)
    # создание экземпляра класса DieselCommand
    diesel = DieselCommand(mqttc)
    # чтение файла с топиками
    topic_victron = data_path.open_json("data_topics_client.json")
    # публикация адреса имитаторов
    publish.push_name_socket(emulators_contact_one, "em_1")
    # publish.push_name_socket(emulators_contact_two, "em_2")
    data_path.open_csv('log_victron.csv', 'w', ['topic', 'value', 'time'])
    # список асинхронных задач
    tasks_callback = [
        victron.callback_data(data_path.open_json("data_topics_victron.json")),
        victron.callback_data_all(data_path.open_csv),
        emulators_callback_one.callback_data(),
        # emulators_callback_two.callback_data(),
        # diesel_callback.callback_data()
    ]
    # запуск списка асинхронных задач
    await asyncio.gather(*tasks_callback)
    condition_em = False
    # цикл для обработки событий
    try:
        while True:
            connect = add_user()
            if command_operator.check_connections(connect):
                if not condition_em:
                    emulators_callback_one.push_command({"on_off": 1})
                    condition_em = True
                # опрос виктрона
                victron.survey_victron()
                # публикация по топикам викторона
                victron.publish_topic(topic_victron)
                # извлечение данных с имитаторов
                emulators_contact_one.get_data_emulators()
                # emulators_contact_two.get_data_emulators()
                # публикация данных с имитаторов
                publish.publish_data_emulators(emulators_contact_one)
                # publish.publish_data_emulators(emulators_contact_two)
                # задержка 1 сек
                await asyncio.sleep(1)
            else:
                print("STOP")
                if condition_em:
                    emulators_callback_one.push_command({"on_off": 0})
                    condition_em = False

    except KeyboardInterrupt:
        ContactEmulators.close_socket(emulators_contact_one.socket)
        # ContactEmulators.close_socket(emulators_contact_two.socket)

        print("Соединение закрыто по инициативе пользователя")


if __name__ == '__main__':
    init_start()
