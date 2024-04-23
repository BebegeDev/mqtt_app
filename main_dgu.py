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
    flag_start_stop_all = False
    while True:
        while operator.check_connections("start_stop_all"):
            if operator.check_connections("start_stop_diesel"):
                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)
                diesel_callback.ready_auto_launch()
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
                diesel_callback.checking_work_status(slave=2)
                # diesel_callback.checking_work_status(slave=3)
                operator.update_current_power(diesel_callback.get_power_current())
            else:
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
            flag_start_stop_all = True

        else:
            if flag_start_stop_all:
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
                operator.update_control_signal('start_stop_diesel', 0)
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
                diesel_callback.checking_work_status(slave=2)
                operator.update_current_power(diesel_callback.get_power_current())
                # diesel_callback.checking_work_status(slave=3)
                flag_start_stop_all = False


if __name__ == '__main__':
    init_start()
