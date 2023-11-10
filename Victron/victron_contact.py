import asyncio
from Interface.interface import InterfaceCallback
import configparser
import json
import os


class VictronCommand(InterfaceCallback):


    def __init__(self, mqttc):
        self.flag_parsed_data = False
        self.parsed_data = None
        self.dictionary = None
        self.flag_get_data = False
        self.dict_msg = {}
        self.mqttc = mqttc

    async def survey_victron(self):
        self.mqttc.publish('R/d436391ea13a/keepalive/', 'empty')
        await asyncio.sleep(60)

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
