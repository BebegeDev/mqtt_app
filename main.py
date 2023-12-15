import asyncio
import time

from Connected.contact_mqtt import connection
from Connected.connection_db import DatabaseConnectionThread
from Diesel.diesel_command import DieselCommand
from Diesel.diesel_contact import DieselContact
from utils.create_file_and_path import Util
from utils.publish import Publish
from Emulators.emulators_contact import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Diesel.diesel_callback import DieselCallback
from Emulators.emulators_callback import EmCallback

from Victron.victron_contact import VictronCommand


async def process_data():
    mqttc = connection()
    main_db = DatabaseConnectionThread().connections_db()

    data_path = Util()
    publish = Publish(mqttc)

    emulators_contact_one = ContactEmulators("EM_ONE")
    emulators_contact_two = ContactEmulators("EM_TWO")
    diesel_contact = DieselContact()

    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))

    emulators_command_one = CommandEmulators(emulators_contact_one)
    emulators_command_two = CommandEmulators(emulators_contact_two)
    diesel_command = DieselCommand(diesel_contact)

    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    emulators_callback_two = EmCallback(mqttc, emulators_contact_two, emulators_command_two)
    diesel_callback = DieselCallback(mqttc, diesel_command)

    victron = VictronCommand(mqttc)
    diesel = DieselCommand(mqttc)

    topic_victron = data_path.open_json("data_topics_client.json")

    publish.push_name_socket(emulators_contact_one, "em_1")
    publish.push_name_socket(emulators_contact_two, "em_2")

    tasks_callback = [
        victron.callback_data(data_path.open_json("data_topics_victron.json")),
        emulators_callback_one.callback_data(),
        emulators_callback_two.callback_data(),
        diesel_callback.callback_data()
    ]

    await asyncio.gather(*tasks_callback)
    try:
        while True:
            victron.survey_victron()
            victron.publish_topic(topic_victron)
            emulators_contact_one.get_data_emulators()
            emulators_contact_two.get_data_emulators()
            publish.publish_data_emulators(emulators_contact_one)
            publish.publish_data_emulators(emulators_contact_two)
            await asyncio.sleep(1)


    except KeyboardInterrupt:
        ContactEmulators.close_socket(emulators_contact_one.socket)
        ContactEmulators.close_socket(emulators_contact_two.socket)

        print("Соединение закрыто по инициативе пользователя")


if __name__ == '__main__':
    asyncio.run(process_data())
