import time
import mqtt.contact_mqtt
import Emulators.command_emulators
import Emulators.contact_emulators
import Victron.victron_comand
from sys import platform


def main():
    mqttc = mqtt.contact_mqtt.connection()
    time.sleep(1)
    emulators = Emulators.command_emulators.CommandEmulators()
    victron = Victron.victron_comand.VictronCommand(mqttc)
    topics_victron = ''
    topics_client = ''
    if platform == 'win32' or platform == 'win64':
        topics_victron = victron.open_json("\\utils\\data_topics_victron.json")
        topics_client = victron.open_json("\\utils\\data_topics_client.json")
    elif platform == 'linux' or platform == 'linux2':
        topics_victron = victron.open_json("/utils/data_topics_victron.json")
        topics_client = victron.open_json("/utils/data_topics_client.json")
    print('Прослушивание R/d436391ea13a/keepalive/')
    try:
        while True:
            time.sleep(5)
            victron.survey_victron(mqttc)
            emulators.get_data_emulators(mqttc)
            for key, item in topics_victron.items():
                mqttc.message_callback_add(item, victron.get_data_victron)
            print(victron.dict_msg)
            for key, item in victron.dict_msg.items():
                mqttc.publish(
                    topics_client[key], item
                )


    except KeyboardInterrupt:
        Emulators.contact_emulators.ContactEmulators.close_socket(emulators.supplySocket_1)
        Emulators.contact_emulators.ContactEmulators.close_socket(emulators.supplySocket_2)
        print("Соединение закрыто по инициативе пользователя")



if __name__ == '__main__':
    main()
