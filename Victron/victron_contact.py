from Interface.interface import InterfaceCallback
import json
import datetime


class VictronCommand(InterfaceCallback):

    def __init__(self, mqttc):
        self.parsed_data_two = None
        self.flag_parsed_data = False
        self.parsed_data = None
        self.dictionary = None
        self.flag_get_data = False
        self.dict_msg = {}
        self.mqttc = mqttc

    def survey_victron(self):
        self.mqttc.publish('R/d436391ea13a/keepalive/', 'empty')

    def get_data(self, client, userdata, data):
        try:
            parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
            self.dictionary = json.loads(data.payload.decode("utf-8", "ignore"))
            self.dict_msg[data.topic] = self.dictionary['value']
            self.validate_data(data)
            if self.flag_get_data:
                self.parsed_data = parsed_data
                self.flag_parsed_data = True
            else:
                print("Получена пустая полезная нагрузка:", data.topic)

        except json.JSONDecodeError as e:
            print("Error: ", e)

    async def callback_data_all(self, log_victron, topic="N/d436391ea13a/#"):
        self.log_victron = log_victron
        self.mqttc.message_callback_add(topic, self.get_data_all)

    def get_data_all(self, client, userdata, data):
        try:
            parsed_data = json.loads(data.payload.decode("utf-8", "ignore"))
            self.validate_data(data)
            if self.flag_get_data:
                self.log_victron('log_victron.csv', 'a', [data.topic, parsed_data, f"time {datetime.datetime.now()}"])
            else:
                print("Получена пустая полезная нагрузка:", data.topic)

        except json.JSONDecodeError as e:
            print("Error: ", e, data.topic)

    async def callback_data(self, topic):
        for key, item in topic.items():
            self.mqttc.message_callback_add(item, self.get_data)

    def publish_topic(self, topics_client):
        for key, item in self.dict_msg.items():
            self.mqttc.publish(
                topics_client[key], item
            )

    def validate_data(self, data):
        if data:
            self.flag_get_data = True
            return True
