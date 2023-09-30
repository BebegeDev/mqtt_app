import configparser
import json
import os
import socket
import re
from sys import platform


class ContactEmulators:

    def __init__(self, mqttc):
        self.mqttc = mqttc
        self.supplySocket_2 = None
        self.supplySocket_1 = None
        self.config = configparser.ConfigParser()
        self.sockets = []
        self.validSrcList = ["front", "web", "seq", "eth", "slot1", "slot2", "slot3", "slot4", "loc", "rem"]
        self.command_list = ["MEAS:VOL?", "MEAS:CUR?", "MEAS:POW?"]
        self.connection_sim()


    @staticmethod
    def send_command(msg, supplySocket):
        msg = msg + "\n"
        supplySocket.sendall(msg.encode("UTF-8"))

    def set_prog_source_v(self, src):
        retval = 0
        if src in self.validSrcList:
            self.send_command("SYST:REM:CV {0}".format(src), self.sockets[0])
            self.send_command("SYST:REM:CV {0}".format(src), self.sockets[1])

        else:
            retval = -1
        return retval


    def set_prog_source_i(self, src):
        retval = 0
        if src.lower() in self.validSrcList:
            self.send_command("SYST:REM:CC {0}".format(src), self.sockets[0])
            self.send_command("SYST:REM:CC {0}".format(src), self.sockets[1])
        else:
            retval = -1
        return retval


    @staticmethod
    def close_socket(supply_socket):
        print("closed socket ", supply_socket)
        supply_socket.shutdown(socket.SHUT_RDWR)
        supply_socket.close()

    def __connect_sockets(self, socket_params_list, timeout_seconds):
        for params in socket_params_list:
            print(f"Подключение к имитатору: {params}")
            ip, port = params
            try:
                supplySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                supplySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                supplySocket.connect((ip, port))
                supplySocket.settimeout(timeout_seconds)
                self.sockets.append(supplySocket)

                print(f"Успешное подключение к {params}")
                print(f"------------------------------------------------------------------")
            except (ConnectionRefusedError, TimeoutError) as e:
                print(f"Ошибка {e} при подключении к {params}")
                print(f"------------------------------------------------------------------")
                self.sockets.append('0')
        return self.sockets


    def send_and_receive_command(self, msg, supplySocket):
        msg = msg + "\n"
        supplySocket.sendall(msg.encode("UTF-8"))
        buffer_size = self.config["EM"]["BUFFER_SIZE"]
        try:
            return re.findall(r'\d+\.\d+', supplySocket.recv(int(buffer_size)).decode())
        except TimeoutError as e:
            print(e)

    def connection_sim(self):
        if platform == 'win32' or platform == 'win64':
            current_script_path = os.path.abspath(__file__)
            project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "\\utils\\setting.ini"
            self.config.read(project_root_path)
        elif platform == 'linux' or platform == 'linux2':
            current_script_path = os.path.abspath(__file__)
            project_root_path = os.path.dirname(os.path.dirname(current_script_path)) + "/utils/setting.ini"
            self.config.read(project_root_path)
        ip_1 = self.config["EM"]["IP_1"]
        ip_2 = self.config["EM"]["IP_2"]
        port_1 = int(self.config["EM"]["PORT"])
        port_2 = int(self.config["EM"]["PORT"])
        timeout = int(self.config["EM"]["TIMEOUT_SECONDS"])
        self.supplySocket_1, self.supplySocket_2 = self.__connect_sockets(
            [
                [ip_1, port_1], [ip_2, port_2]
            ], timeout
        )

    def get_data_emulators(self):
        if self.supplySocket_1 != "0":
            try:
                result = self.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.supplySocket_1)
                power = float(result[0]) * float(result[1])
                print("Имитатор 1:")
                print("-------Напряжение: ", result[0])
                print("-------Ток: ", result[1])
                print("-------Напряжение: ", power)
                self.mqttc.publish('mpei/Emulator1/Volt', payload=json.dumps({"value": result[0]}))
                self.mqttc.publish('mpei/Emulator1/Current', payload=json.dumps({"value": result[1]}))
                self.mqttc.publish('mpei/Emulator1/Power', payload=json.dumps({"value": power}))
            except TypeError:
                print(f"Выходные параметры {self.supplySocket_1} являются типа None")
        else:
            self.mqttc.publish('mpei/Emulator1/Volt', payload=json.dumps({"value": 0}))
            self.mqttc.publish('mpei/Emulator1/Current', payload=json.dumps({"value": 0}))
            self.mqttc.publish('mpei/Emulator1/Power', payload=json.dumps({"value": 0}))

        if self.supplySocket_2 != "0":
            try:
                result = self.send_and_receive_command("MEAS:VOL?\nMEAS:CUR?", self.supplySocket_2)
                power = float(result[0]) * float(result[1])
                print("Имитатор 2:")
                print("-------Напряжение: ", result[0])
                print("-------Ток: ", result[1])
                print("-------Напряжение: ", power)
                self.mqttc.publish('mpei/Emulator2/Volt', payload=json.dumps({"value": result[0]}))
                self.mqttc.publish('mpei/Emulator2/Current', payload=json.dumps({"value": result[1]}))
                self.mqttc.publish('mpei/Emulator2/Power', payload=json.dumps({"value": power}))
            except TypeError:
                print(f"Выходные параметры {self.supplySocket_2} являются типа None")
        else:
            self.mqttc.publish('mpei/Emulator2/Volt', payload=json.dumps({"value": 0}))
            self.mqttc.publish('mpei/Emulator2/Current', payload=json.dumps({"value": 0}))
            self.mqttc.publish('mpei/Emulator2/Power', payload=json.dumps({"value": 0}))


