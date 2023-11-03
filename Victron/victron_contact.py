import asyncio

import configparser
import json
import os


class VictronCommand:

    def __init__(self, mqttc):
        self.dictionary = None
        self.dict_msg = {}
        self.mqttc = mqttc

    def survey_victron(self):
        self.mqttc.publish('R/d436391ea13a/keepalive/', 'empty')

    def get_data_victron(self, client, userdata, msg):
        if msg.payload:
            try:
                self.dictionary = json.loads(msg.payload.decode("utf-8", "ignore"))
                self.dict_msg[msg.topic] = self.dictionary['value']
            except json.JSONDecodeError as e:
                print("Error: ", e)
        else:
            print("Получена пустая полезная нагрузка:", msg.topic)


    @staticmethod
    def open_json(path):
        current_script_path = os.path.abspath(__file__)
        project_root_path = os.path.dirname(os.path.dirname(current_script_path))+path
        with open(project_root_path, 'r') as json_file:
            topics = json.load(json_file)
        return topics

    async def callback_topics(self, topic):
        for key, item in topic.items():
            self.mqttc.message_callback_add(item, self.get_data_victron)

    def publish_topic(self, topics_client):
        for key, item in self.dict_msg.items():
            self.mqttc.publish(
                topics_client[key], item
            )
