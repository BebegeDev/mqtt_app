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
    connect = add_user()
    operator = Command(mqttc, connect)
    operator.callback_data()
    while True:
        if operator.check_connections():
            print(operator.get_param_em())
            asyncio.run(process_data(mqttc, operator))
            break


async def process_data(mqttc, operator):
    print("START INIT")
    data_path = Util()
    publish = Publish(mqttc)
    emulators_contact_one = ContactEmulators("EM_ONE")
    # emulators_contact_two = ContactEmulators("EM_TWO")
    # diesel_contact = DieselContact()
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    # emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_command_one = CommandEmulators(emulators_contact_one.socket)
    # emulators_command_two = CommandEmulators(emulators_contact_two)
    # diesel_command = DieselCommand(diesel_contact)
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    # emulators_callback_two = EmCallback(mqttc, emulators_contact_two)
    # diesel_callback = DieselCallback(mqttc, diesel_command)
    victron = VictronCommand(mqttc)
    diesel = DieselCommand(mqttc)
    topic_victron = data_path.open_json("data_topics_client.json")
    publish.push_name_socket(emulators_contact_one, "em_1")
    # publish.push_name_socket(emulators_contact_two, "em_2")
    data_path.open_csv('log_victron.csv', 'w', ['topic', 'value', 'time'])

    tasks_callback = [
        victron.callback_data(data_path.open_json("data_topics_victron.json")),
        victron.callback_data_all(data_path.open_csv),
        emulators_callback_one.callback_data(),
        # emulators_callback_two.callback_data(),
        # diesel_callback.callback_data()
    ]

    await asyncio.gather(*tasks_callback)
    condition_em = False
    emulators_callback_one.push_command({
        # "on_off": 1,
        "SYST:INT:SIM:SET VOC_STC,": operator.get_param_em()[1],
        "SYST:INT:SIM:SET ISC_STC,": operator.get_param_em()[2],
        "SYST:INT:SIM:SET VMPP_STC,": operator.get_param_em()[3],
        "SYST:INT:SIM:SET IMPP_STC,": operator.get_param_em()[4],
        "SYST:INT:SIM:SET ALPHA,": operator.get_param_em()[5],
        "SYST:INT:SIM:SET BETA,": operator.get_param_em()[6]
    })
    try:
        while True:
            if operator.check_connections():
                if not condition_em:
                    print("START")
                    condition_em = True
                victron.survey_victron()
                victron.publish_topic(topic_victron)
                emulators_contact_one.get_data_emulators()
                # emulators_contact_two.get_data_emulators()
                publish.publish_data_emulators(emulators_contact_one)
                # publish.publish_data_emulators(emulators_contact_two)
                await asyncio.sleep(1)
            else:
                if condition_em:
                    print("STOP")
                    # emulators_callback_one.push_command({"on_off": 0})
                    condition_em = False
                    await asyncio.sleep(1)

    except KeyboardInterrupt:
        ContactEmulators.close_socket(emulators_contact_one.socket)
        # ContactEmulators.close_socket(emulators_contact_two.socket)
        print("Соединение закрыто по инициативе пользователя")


if __name__ == '__main__':
    init_start()
