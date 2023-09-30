import time
import mqtt.contact_mqtt
import Emulators.emulators_command
import Emulators.emulators_contact
import Victron.victron_contact
import Diesel.diesel_contact
from sys import platform


def main():
    mqttc = mqtt.contact_mqtt.connection()
    time.sleep(1)
    emulators_contact = Emulators.emulators_contact.ContactEmulators(mqttc)
    emulators_command = Emulators.emulators_command.CommandEmulators(mqttc, emulators_contact)
    victron = Victron.victron_contact.VictronCommand(mqttc)
    diesel = Diesel.diesel_contact.DieselCommand(mqttc)
    topics_victron = ''
    topics_client = ''
    topics_diesel = ''
    if platform == 'win32' or platform == 'win64':
        topics_victron = victron.open_json("\\utils\\data_topics_victron.json")
        topics_client = victron.open_json("\\utils\\data_topics_client.json")
        topics_diesel = diesel.open_json("\\utils\\data_topics_diesel.json")
    elif platform == 'linux' or platform == 'linux2':
        topics_victron = victron.open_json("/utils/data_topics_victron.json")
        topics_client = victron.open_json("/utils/data_topics_client.json")
        topics_diesel = diesel.open_json("/utils/data_topics_diesel.json")
        diesel.publish_topic(topics_diesel)
    print('Прослушивание R/d436391ea13a/keepalive/')
    try:
        while True:
            time.sleep(5)
            victron.survey_victron()
            emulators_contact.get_data_emulators()
            victron.callback_topics(topics_victron)
            victron.publish_topic(topics_client)



    except KeyboardInterrupt:
        Emulators.emulators_contact.ContactEmulators.close_socket(emulators_contact.supplySocket_1)
        Emulators.emulators_contact.ContactEmulators.close_socket(emulators_contact.supplySocket_2)
        print("Соединение закрыто по инициативе пользователя")



if __name__ == '__main__':
    main()
