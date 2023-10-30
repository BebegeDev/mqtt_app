import json
import os

# pref = "N/d436391ea13a"
# topics = {
#     "PV_battery_voltage": pref+"/system/0/Dc/Battery/Voltage",
#     "PV_battery_power": pref+"/system/0/Dc/Battery/Power",
#     "PV_battery_current": pref+"/system/0/Dc/Battery/Current",
#     "PV_soc": pref+"/system/0/Dc/Battery/Soc",
#     "PV_ac_consumption": pref+"system/0/Ac/Consumption/L1/Power",
#     "PV_power": pref+"/system/0/Dc/Pv/Power",
#     "PV_generator": pref+"/system/0/Ac/Genset/L1/Power",
#     "Power Generated Today": pref+"/solarcharger/256/History/Daily/0/Yield",
#     "Power Generated Total": pref+"/solarcharger/256/Yield/System"
# }
# current_script_path = os.path.abspath(__file__)
# project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\data_topics_client.json"
#
# with open(project_root_path, "w") as json_file:
#     json.dump(topics, json_file)

# pref = "mpei/Victron/"
# topics = {
#     "PV_battery_voltage": pref+"PV_battery_voltage",
#     "PV_battery_power": pref+"PV_battery_power",
#     "PV_battery_current": pref+"PV_battery_current",
#     "PV_soc": pref+"PV_soc",
#     "PV_ac_consumption": pref+"PV_ac_consumption",
#     "PV_power": pref+"PV_power",
#     "PV_generator": pref+"PV_generator",
#     "Power Generated Today": pref+"Power Generated Today",
#     "Power Generated Total": pref+"Power Generated Total"
# }
# current_script_path = os.path.abspath(__file__)
# project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\data_topics_client.json"
#
# with open(project_root_path, "w") as json_file:
#     json.dump(topics, json_file)

# pref = "mpei/DGU/"


# def diesel(d):
#     return {
#         "power": [f'{pref}{d}/power/set_point', f'{pref}{d}/power/rated_power', f'{pref}{d}/power'
#                                                                                 f'/current_generator_power'],
#         "job_status": [f"{pref}{d}/job_status"],
#         "autorun": [f"{pref}{d}/autorun"],
#         "voltage/frequency": [f"{pref}{d}/voltage_frequency"]
#     }
#
#
# topics = []
# for i in range(1, 7):
#     topics.append(diesel(i))
# current_script_path = os.path.abspath(__file__)
# project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\data_topics_diesel.json"
#
# with open(project_root_path, "w") as json_file:
#     json.dump(topics, json_file)

