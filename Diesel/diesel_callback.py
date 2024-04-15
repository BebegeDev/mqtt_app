import json
import time

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

    def checking_work_status(self, address=3, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)
        print("Статус работы:", status[0])

    def ready_auto_launch(self, address=31, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)
        print("Готовность к авто-запуску:", status[0])

    def on_off(self, available_dgu, slave, value=True):
        if available_dgu:
            address = 0
        else:
            address = 3
        self.diesel.command_write_coil(address, value, slave)
        print(f"Отправлена команда на slave {slave} address {address}")

    def command_processing_diesel(self, status, available_dgu):
        if status:

            if self.flag:
                print("Включение ДГУ №2")
                self.on_off(available_dgu, slave=2)
                self.flag = False
                time.sleep(10)
                self.diesel.command_write_coil(24, True, 2)
        else:

            if not self.flag:
                self.diesel.command_write_coil(25, True, 2)
                print("Останов ДГУ №2")
                self.on_off(available_dgu, slave=2)
                self.flag = True

