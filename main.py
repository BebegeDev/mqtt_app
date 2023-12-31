import asyncio
import time

from mqtt.contact_mqtt import connection
from Diesel.diesel_command import DieselCommand
from utils.create_file_and_path import Util
from utils.publish import Publish
from Emulators.emulators_contact import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Emulators.emulators_callback import EmCallback

from Victron.victron_contact import VictronCommand


async def process_data():
    mqttc = connection()
    time.sleep(1)

    data_path = Util()
    publish = Publish(mqttc)
    emulators_contact_one = ContactEmulators(mqttc, "EM_ONE")
    emulators_contact_two = ContactEmulators(mqttc, "EM_TWO")
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))

    emulators_command_one = CommandEmulators(emulators_contact_one)
    emulators_command_two = CommandEmulators(emulators_contact_two)
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    victron = VictronCommand(mqttc)
    diesel = DieselCommand(mqttc)
    topic_victron = data_path.open_json("data_topics_client.json")
    tasks_callback = [victron.callback_data(data_path.open_json("data_topics_victron.json")),
                      emulators_callback_one.callback_data()]

    await asyncio.gather(*tasks_callback)
    try:
        while True:

            await victron.survey_victron()

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
