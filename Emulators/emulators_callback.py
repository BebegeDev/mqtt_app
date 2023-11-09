import json

from Interface.interface import InterfaceCallback


class EmCallback(InterfaceCallback):

    def __init__(self, mqttc, em, emulators_command_one):
        self.flag_get_data = None
        self.em = em
        self.mqttc = mqttc
        self.emulators_command_one = emulators_command_one

    async def callback_data(self, topic="mpei/Operator/Command"):
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        try:
            parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
            self.validate_data(data)
            if self.flag_get_data:
                self.test(parsed_data)
        except Exception as e:
            print(f"Error {e}")

    def validate_data(self, data):
        if data:
            self.flag_get_data = True

    def test(self, msg):
        key = list(msg.keys())[0]
        dict_command = {
            'test2': self.emulators_command_one.test2,
            'on_off': self.emulators_command_one.on_off,
            'set_voltage': self.emulators_command_one.set_voltage,
            'set_current': self.emulators_command_one.set_current,
        }
        func = dict_command[key]
        func(msg)
