import asyncio

from Connected.contact_mqtt import connection
# from Connected.connection_db import DatabaseConnectionThread
from Diesel.diesel_command import DieselCommand
from Connected.diesel_contact import DieselContact
from utils.create_file_and_path import Util
from utils.publish import Publish
from Connected.emulators_connect import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Diesel.diesel_callback import DieselCallbackBD
from Emulators.emulators_callback import EmCallback
from Victron.victron_contact import VictronCommand
from Request.command_operator import Command
from Connected.connection_db import add_user


def init_start():
    mqttc = connection()
    connect = add_user()
    operator = Command(mqttc, connect)
    operator.callback_data()
    while True:
        if operator.check_connections("start_stop_all"):
            try:
                asyncio.run(process_data(mqttc, operator))
            finally:
                print("Останов программы")
            break


async def process_data(mqttc, operator):
    print("START INIT")
    data_path = Util()
    publish = Publish(mqttc)
    emulators_contact_one = ContactEmulators("EM_ONE")
    # emulators_contact_two = ContactEmulators("EM_TWO")
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    # emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_command_one = CommandEmulators(emulators_contact_one.socket)
    # emulators_command_two = CommandEmulators(emulators_contact_two)
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    # emulators_callback_two = EmCallback(mqttc, emulators_contact_two)
    victron = VictronCommand(mqttc)
    topic_victron = data_path.open_json("data_topics_client.json")
    publish.push_name_socket(emulators_contact_one, "em_1")
    # publish.push_name_socket(emulators_contact_two, "em_2")
    data_path.open_csv('log_victron.csv', 'w', ['topic', 'value', 'time'])
    diesel_contact = DieselContact()
    diesel_command = DieselCommand(diesel_contact.client)
    diesel_callback = DieselCallbackBD(diesel_command)
    em_param = operator.get_param_em(tables="parameters_pv")
    emulators_callback_one.push_command({
        "SYST:INT:SIM:SET VOC_STC,": em_param[1],
        "SYST:INT:SIM:SET ISC_STC,": em_param[2],
        "SYST:INT:SIM:SET VMPP_STC,": em_param[3],
        "SYST:INT:SIM:SET IMPP_STC,": em_param[4],
        "SYST:INT:SIM:SET ALPHA,": em_param[5],
        "SYST:INT:SIM:SET BETA,": em_param[6]
    })

    tasks_callback = [
        victron.callback_data(data_path.open_json("data_topics_victron.json")),
        victron.callback_data_all(data_path.open_csv),
        emulators_callback_one.callback_data(),
        # emulators_callback_two.callback_data(),
        # diesel_callback.callback_data()
    ]

    await asyncio.gather(*tasks_callback)
    print("Инициализация прошла успешно")
    while True:
        if operator.check_connections("start_stop_all"):
            emulators_callback_one.command_processing_em(operator.check_connections("start_stop_em"),
                                                         "OUTPUT,", 1)
            # emulators_callback_one.command_processing_em(True,
            #                                              "SYST:INT:SIM"
            #                                              ":SET TSTC,", operator.get_param_em(tables="simulator_1")[3])
            # emulators_callback_one.command_processing_em(True,
            #                                              "SYST:INT:SIM"
            #                                              ":SET GSTC,", operator.get_param_em(tables="simulator_1")[2])

            if diesel_contact.client.connect():
                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)
                diesel_callback.ready_auto_launch()
                available_dgu = operator.get_available_dgu()
                diesel_callback.command_processing_diesel(operator.check_connections("start_stop_diesel"), available_dgu[0])

                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)

            victron.survey_victron()
            victron.publish_topic(topic_victron)
            emulators_contact_one.get_data_emulators()
            # emulators_contact_two.get_data_emulators()
            publish.publish_data_emulators(emulators_contact_one)
            # publish.publish_data_emulators(emulators_contact_two)
        else:
            print("STOP")
            emulators_callback_one.command_processing_em(False, "OUTPUT,", 0)
            diesel_callback.command_processing_diesel(operator.check_connections("start_stop_all"), 0)
            diesel_callback.checking_work_status(slave=2)
            # diesel_callback.checking_work_status(slave=3)
        try:
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            print("Отмена обработки асинхронной операции")
            ContactEmulators.close_socket(emulators_contact_one.socket)
            # ContactEmulators.close_socket(emulators_contact_two.socket)
            break


if __name__ == '__main__':
    init_start()
