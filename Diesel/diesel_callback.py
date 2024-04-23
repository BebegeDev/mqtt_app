import json
import time
from datetime import datetime

from Interface.interface import InterfaceCallback


class DieselCallbackMQTT(InterfaceCallback):

    def __init__(self, diesel, mqttc):
        self.mqttc = mqttc
        self.diesel = diesel

    def callback_data(self, topic="mpei/commands_operator/diesel"):
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
        self.validate_data(data)
        self.push_command(parsed_data)

    def validate_data(self, data):
        pass

    def push_command(self, msg):
        key = list(msg.keys())
        value = list(msg.values())
        print(key)
        print(value)
        dict_command = {
            'command_write_registers': [self.diesel.command_write_registers(value[1],
                                                                            value[2],
                                                                            value[3])],
            'command_read_holding_registers': [self.diesel.command_read_holding_registers(value[1],
                                                                                          value[2],
                                                                                          value[3])],
            'command_read_input_registers': [self.diesel.command_read_input_registers(value[1],
                                                                                      value[2],
                                                                                      value[3])],
            'get_data_bool': [self.diesel.get_data_bool(value[1],
                                                        value[2],
                                                        value[3])],
            'command_write_coil': [self.diesel.command_write_coil(value[1],
                                                                  value[2],
                                                                  value[3])]
        }
        func, command = dict_command[key]
        func(command)


class DieselCallbackBD:

    def __init__(self, diesel):
        self.flag = True
        self.diesel = diesel
        self.old_command = 0
        self.old_list_command = []

    def checking_work_status(self, address=3, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)
        # print("Статус работы:", status[0])

    def ready_auto_launch(self, address=31, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)
        # print("Готовность к авто-запуску:", status[0])

    def get_power_current(self):
        return self.diesel.command_read_input_registers(address=519, count=1, slave=2)

    def on_off(self, available_dgu, slave, value=True):
        if available_dgu:
            address = 0
        else:
            address = 3
        self.diesel.command_write_coil(address, value, slave)
        print(f"Отправлена команда на slave {slave} address {address} {datetime.now()}")

    def command_processing_diesel(self, available_dgu):
        for dgu in available_dgu:
            if dgu not in self.old_list_command:
                self.on_off(dgu['control_dgu'], slave=dgu['slave'])
        self.old_list_command = available_dgu
