from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Connected.emulators_connect import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Emulators.emulators_callback import EmCallback
from Request.command_operator import Command
from utils.create_file_and_path import Util
from utils.publish import Publish


def init_start():
    mqttc = connection()
    connect = add_user()
    operator = Command(mqttc, connect)
    data_path = Util()
    publish = Publish(mqttc)
    emulators_contact_one = ContactEmulators("EM_ONE")
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_command_one = CommandEmulators(emulators_contact_one.socket)
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)
    publish.push_name_socket(emulators_contact_one, "em_1")
    em_param = operator.get_param_em(tables="parameters_pv")
    emulators_callback_one.push_command({
        "SYST:INT:SIM:SET VOC_STC,": em_param[1],
        "SYST:INT:SIM:SET ISC_STC,": em_param[2],
        "SYST:INT:SIM:SET VMPP_STC,": em_param[3],
        "SYST:INT:SIM:SET IMPP_STC,": em_param[4],
        "SYST:INT:SIM:SET ALPHA,": em_param[5],
        "SYST:INT:SIM:SET BETA,": em_param[6],
        "SYST:INT:SIM:SET TSTC,": 25,
        "SYST:INT:SIM:SET GSTC,": 1000
    })
    emulators_callback_one.callback_data()
    while True:
        if operator.check_connections("start_stop_all"):
            emulators_callback_one.command_processing_em(operator.check_connections("start_stop_em"),
                                                         "OUTPUT, ", operator.check_connections("start_stop_em"))
            emulators_callback_one.command_processing_em(operator.check_connections("start_stop_em"),
                                                         "SYST:INT:SIM:SET TPV,",
                                                         operator.get_param_em(tables="simulator_1")[3])
            emulators_callback_one.command_processing_em(operator.check_connections("start_stop_em"),
                                                         "SYST:INT:SIM:SET GPV,",
                                                         operator.get_param_em(tables="simulator_1")[2])
            emulators_contact_one.get_data_emulators()
            publish.publish_data_emulators(emulators_contact_one)
        else:
            emulators_callback_one.command_processing_em(False, "OUTPUT, ", 0)


if __name__ == '__main__':
    init_start()
