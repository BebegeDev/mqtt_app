import json

from Interface.interface import InterfaceCallback


class EmCallback(InterfaceCallback):

    def __init__(self, mqttc, em, em_command):
        self.flag_get_data = None
        self.em = em
        self.mqttc = mqttc
        self.em_command = em_command
        self.flag = True

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

    def command_out(self, msg):

        for key, value in msg.items():
            command = f"{key} {value}"
            self.em_command.send_command(command)

    def push_command(self, msg):
        self.em_command.set_prog_source_v("eth")
        self.em_command.set_prog_source_i("eth")
        for key, value in msg.items():
            command = f"{key}{value}"
            self.em_command.send_command(command)
        self.em_command.set_prog_source_v("slot4")
        self.em_command.set_prog_source_i("slot4")

    def command_processing_em(self, status, command, value):
        if status:

            if self.flag:
                self.command_out({
                    command: status,
                })
                self.flag = False
        else:
            if not self.flag:
                self.command_out({
                    command: status,
                })
                self.flag = True
