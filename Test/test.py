# from Emulators.emulators_logics_command import EmulatorsLogicsCommand
# import asyncio
# from mqtt.contact_mqtt import connection
# from Diesel.diesel_command import DieselCommand
# from utils.create_file_and_path import Util
# from utils.publish import Publish
# from Emulators.emulators_contact import ContactEmulators
# from Emulators.emulators_command import CommandEmulators
# from Victron.victron_contact import VictronCommand
#
#
# async def process_data():
#     mqttc = connection()
#     emulators_contact_one = ContactEmulators(mqttc, "EM_ONE")
#     emulators_command_one = CommandEmulators(mqttc, emulators_contact_one)
#
#     tasks_callback = [emulators_command_one.callback_data()]
#     await asyncio.gather(*tasks_callback)
#
#     while True:
#         pass
#
#
# if __name__ == '__main__':
#     asyncio.run(process_data())
