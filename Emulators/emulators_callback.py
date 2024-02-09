import json

from Interface.interface import InterfaceCallback


class EmCallback(InterfaceCallback):

    def __init__(self, mqttc, em):
        self.flag_get_data = None
        self.em = em
        self.mqttc = mqttc

    async def callback_data(self, topic="mpei/command_operator/em"):
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):

        parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
        self.validate_data(data)
        if self.flag_get_data:
            self.push_command(parsed_data)

    def validate_data(self, data):
        if data:
            self.flag_get_data = True

    def push_command(self, msg):
        key = list(msg.keys())[0]
        value = list(msg.values())[0]
        print(key)
        print(value)
        dict_command = {
            'test2': [self.em.test2, 1],
            'on_off': [self.em.on_off, f"OUTPUT {value}"],
            'set_voltage': [self.em.set_point_command, f"SOUR:VOLT {value}"],
            'set_current': [self.em.set_point_command, f"SOUR:CUR {value}"]
        }
        func, command = dict_command[key]
        func(command)
