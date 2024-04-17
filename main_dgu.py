from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Diesel.diesel_command import DieselCommand
from Diesel.diesel_callback import DieselCallbackBD
from Connected.diesel_contact import DieselContact
from Request.command_operator import Command


def init_start():
    mqttc = connection()
    connect = add_user()
    operator = Command(mqttc, connect)
    diesel_contact = DieselContact()
    diesel_command = DieselCommand(diesel_contact.client)
    diesel_callback = DieselCallbackBD(diesel_command)
    while True:
        if operator.check_connections("start_stop_all"):

            while diesel_contact.client.connect():
                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)
                diesel_callback.ready_auto_launch()
                available_dgu = operator.get_available_dgu()
                diesel_callback.command_processing_diesel(operator.check_connections("start_stop_diesel"), available_dgu[0])

                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)

        else:
            diesel_callback.command_processing_diesel(operator.check_connections("start_stop_all"), 0)
            diesel_callback.checking_work_status(slave=2)
            # diesel_callback.checking_work_status(slave=3)


if __name__ == '__main__':
    init_start()
