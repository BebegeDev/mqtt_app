import time

from Connected.contact_mqtt import connection
from Victron.victron_contact import VictronCommand
from utils.create_file_and_path import Util


def init_start():
    mqttc = connection()
    data_path = Util()
    victron = VictronCommand(mqttc)
    topic_victron = data_path.open_json("data_topics_client.json")
    victron.callback_data(data_path.open_json("data_topics_victron.json"))
    victron.callback_data_all(data_path.open_csv)
    while True:
        victron.survey_victron()
        victron.publish_topic(topic_victron)
        time.sleep(2)


if __name__ == '__main__':
    init_start()
